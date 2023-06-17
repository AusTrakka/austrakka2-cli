import hashlib
from loguru import logger

from .errors import WorkflowError
from .sync_io import *
from .state_machine import StateMachine, SName, State, Action
from ..funcs import _get_seq_data
from austrakka.utils.enums.seq import READ_BOTH
from austrakka.utils.enums.seq import BY_IS_ACTIVE_FLAG
from austrakka.components.sequence.funcs import _download_seq_file
from austrakka.components.sequence.funcs import _get_seq_download_path
from austrakka.utils.retry import retry


def configure_state_machine() -> StateMachine:

    # Configure the generic state machine with a list of allowed
    # states and actions (a.k.a transitions). The state machine
    # uses this information to do a cursory check of your handler
    # implementations. E.g. if your handler declares that the next
    # state is 'x' and it is not known, it will raise a runtime
    # exception and halt rather than potentially corrupting your
    # data.
    return StateMachine({
        SName.PULLING_MANIFEST: State(SName.PULLING_MANIFEST),
        SName.DONE_PULLING_MANIFEST: State(SName.DONE_PULLING_MANIFEST),
        SName.ANALYSING: State(SName.ANALYSING),
        SName.DONE_ANALYSING: State(SName.DONE_ANALYSING),
        SName.DOWNLOADING: State(SName.DOWNLOADING),
        SName.DONE_DOWNLOADING: State(SName.DONE_DOWNLOADING),
        SName.FINALISING: State(SName.FINALISING),
        SName.DONE_FINALISING: State(SName.DONE_FINALISING),
        SName.FINALISATION_FAILED: State(SName.FINALISATION_FAILED, is_end_state=True),
        SName.PURGING: State(SName.PURGING),
        SName.DONE_PURGING: State(SName.DONE_PURGING),
        SName.UP_TO_DATE: State(SName.UP_TO_DATE, is_end_state=True),
    }, {
        Action.set_state_pulling_manifest: set_state_pulling_manifest,
        Action.pull_manifest: pull_manifest,
        Action.set_state_analysing: set_state_analysing,
        Action.analyse: analyse,
        Action.set_state_downloading: set_state_downloading,
        Action.download: download,
        Action.set_state_finalising: set_state_finalising,
        Action.finalise: finalise,
        Action.set_state_purging: set_state_purging,
        Action.purge: purge,
        Action.set_state_up_to_date: set_state_up_to_date
    })


def set_state_pulling_manifest(sync_state: dict):
    sync_state[CURRENT_STATE_KEY] = SName.PULLING_MANIFEST
    sync_state[CURRENT_ACTION_KEY] = Action.pull_manifest


def pull_manifest(sync_state: dict):
    logger.info(f'Started: {Action.pull_manifest}')
    data = _get_seq_data(
        sync_state[SEQ_TYPE_KEY],
        READ_BOTH,
        sync_state[GROUP_NAME_KEY],
        BY_IS_ACTIVE_FLAG,
    )

    logger.info(f'Freshly pulled manifest has {len(data)} entries.')
    path = get_path_from_state(sync_state, INTERMEDIATE_MANIFEST_FILE_KEY)
    logger.info(f'Saving to intermediate manifest: {path}')

    with open(path, 'w') as f:
        pd.DataFrame(data).to_csv(f, index=False)

    sync_state[CURRENT_STATE_KEY] = SName.DONE_PULLING_MANIFEST
    sync_state[CURRENT_ACTION_KEY] = Action.set_state_analysing
    logger.info(f'Finished: {Action.pull_manifest}')


def set_state_analysing(sync_state: dict):
    sync_state[CURRENT_STATE_KEY] = SName.ANALYSING
    sync_state[CURRENT_ACTION_KEY] = Action.analyse


def analyse(sync_state: dict):
    logger.info(f'Started: {Action.analyse}')

    df = read_from_csv(sync_state, INTERMEDIATE_MANIFEST_FILE_KEY)
    do_hash_check = (HASH_CHECK_KEY not in sync_state) or \
                    (HASH_CHECK_KEY in sync_state and sync_state[HASH_CHECK_KEY] is True)

    if STATUS_KEY not in df.columns:
        df[STATUS_KEY] = ""

    for index, row in df.iterrows():
        seq_path = os.path.join(
            sync_state[OUTPUT_DIR_KEY],
            str(row[SAMPLE_NAME_KEY]),
            str(row[FILE_NAME_ON_DISK_KEY]))

        analyse_status(df, do_hash_check, index, row, seq_path)

    save_int_manifest(df, sync_state)
    sync_state[CURRENT_STATE_KEY] = SName.DONE_ANALYSING
    sync_state[CURRENT_ACTION_KEY] = Action.set_state_downloading
    logger.success(f'Finished: {Action.analyse}')


def set_state_downloading(sync_state: dict):
    sync_state[CURRENT_STATE_KEY] = SName.DOWNLOADING
    sync_state[CURRENT_ACTION_KEY] = Action.download


def download(sync_state: dict):
    logger.info(f'Started: {Action.download}')

    df = read_from_csv(sync_state, INTERMEDIATE_MANIFEST_FILE_KEY)

    if HOT_SWAP_NAME_KEY not in df.columns:
        df[HOT_SWAP_NAME_KEY] = ""

    save_int_manifest(df, sync_state)

    path = get_path_from_state(sync_state, INTERMEDIATE_MANIFEST_FILE_KEY)
    with open(path, 'w') as f:
        for index, row in df.iterrows():
            if row[STATUS_KEY] != DOWNLOADED and row[STATUS_KEY] != MATCH:
                get_file_from_server(df, index, row, sync_state)

            df.to_csv(f, index=False)
            f.seek(0)
        f.close()

    sync_state[CURRENT_STATE_KEY] = SName.DONE_DOWNLOADING
    sync_state[CURRENT_ACTION_KEY] = Action.set_state_finalising
    logger.success(f'Finished: {Action.download}')


def set_state_finalising(sync_state: dict):
    sync_state[CURRENT_STATE_KEY] = SName.FINALISING
    sync_state[CURRENT_ACTION_KEY] = Action.finalise


def finalise(sync_state: dict):
    logger.info(f'Started: {Action.finalise}')

    int_med = read_from_csv(sync_state, INTERMEDIATE_MANIFEST_FILE_KEY)

    errors = int_med.loc[(int_med[STATUS_KEY] != MATCH) &
                         (int_med[STATUS_KEY] != DOWNLOADED) &
                         (int_med[STATUS_KEY] != DRIFTED)]

    if len(errors.index) > 0:
        im_path = os.path.join(
            sync_state[OUTPUT_DIR_KEY],
            sync_state[INTERMEDIATE_MANIFEST_FILE_KEY])

        logger.error(f'Found entries which are failed or missing after the '
                     f'download stage. Check the intermediate manifest for '
                     f'specific file entries: {im_path}')

        sync_state[CURRENT_STATE_KEY] = SName.FINALISATION_FAILED
        sync_state[CURRENT_ACTION_KEY] = Action.set_state_analysing
        logger.error('Finalise failed.')
    else:
        finalise_each_file(int_med, sync_state)
        publish_new_manifest(int_med, sync_state)
        detect_and_record_obsolete_files(int_med, sync_state)

        sync_state[CURRENT_STATE_KEY] = SName.DONE_FINALISING
        sync_state[CURRENT_ACTION_KEY] = Action.set_state_purging
        logger.success(f'Finished: {Action.finalise}')


def set_state_purging(sync_state: dict):
    sync_state[CURRENT_STATE_KEY] = SName.PURGING
    sync_state[CURRENT_ACTION_KEY] = Action.purge


def purge(sync_state: dict):
    logger.info(f'Started: {Action.purge}')
    logger.info('Nothing to purge..')
    sync_state[CURRENT_STATE_KEY] = SName.DONE_PURGING
    sync_state[CURRENT_ACTION_KEY] = Action.set_state_up_to_date
    logger.success(f'Finished: {Action.purge}')


def set_state_up_to_date(sync_state: dict):
    sync_state[CURRENT_STATE_KEY] = SName.UP_TO_DATE
    sync_state[CURRENT_ACTION_KEY] = Action.set_state_pulling_manifest


def finalise_each_file(int_med, sync_state):
    for index, row in int_med.iterrows():

        dest = os.path.join(
            sync_state[OUTPUT_DIR_KEY],
            int_med.at[index, SAMPLE_NAME_KEY],
            int_med.at[index, FILE_NAME_ON_DISK_KEY])

        if int_med.at[index, STATUS_KEY] == DRIFTED:
            src = os.path.join(
                sync_state[OUTPUT_DIR_KEY],
                int_med.at[index, SAMPLE_NAME_KEY],
                int_med.at[index, HOT_SWAP_NAME_KEY])

            logger.info(f'Hot swapping: {dest}')
            os.rename(src, dest)
            logger.success(f'Done hot swapping: {dest}')

            int_med.at[index, STATUS_KEY] = DONE

        elif int_med.at[index, STATUS_KEY] == MATCH or\
                int_med.at[index, STATUS_KEY] == DOWNLOADED:

            int_med.at[index, STATUS_KEY] = DONE
            logger.success(f'Done: {dest}')

        else:
            raise WorkflowError(f'Reach an impossible state in the depths of {Action.finalise}. '
                                f'Expecting each file state to be only "{MATCH}", '
                                f'"{DOWNLOADED}", or "{DRIFTED}" but got something else. '
                                f'The caller, probably {Action.finalise}, should have checked '
                                f'my inputs before calling me.')

    save_int_manifest(int_med, sync_state)


def detect_and_record_obsolete_files(int_med, sync_state):
    logger.info('Checking for obsolete files..')

    # Get the list of files on disk. The array is a list of (full_path, file_name_only)
    files_on_disk = []
    obsoletes = pd.DataFrame({FILE_PATH_KEY: [], FILE_NAME_KEY: []})
    for (root_dir, dir_names, file_names) in os.walk(sync_state[OUTPUT_DIR_KEY]):
        for f in file_names:
            if os.path.splitext(f)[-1] in [FASTQ_EXT, FASTA_EXT, GZ_EXT]:
                files_on_disk.append((os.path.join(root_dir, f), f))

    # If files found on disk are not in the intermediate manifest,
    # it is added to the list of obsolete files.
    for pair in files_on_disk:
        r = int_med.loc[(int_med[FILE_NAME_ON_DISK_KEY] == pair[-1])]
        if len(r.index) == 0:
            obsoletes.loc[len(obsoletes.index)] = pair

    # Check the reverse direction. If something is on the current obsolete list
    # of file, and is also in the intermediate manifest, then it needs to be
    # removed from the obsolete list. Additionally, if there is already an
    # entry on the obsolete list and still isn't on the intermediate manifest,
    # then it should be left on the obsolete list.
    p = get_path_from_state(sync_state, OBSOLETE_OBJECTS_FILE_KEY)
    if os.path.exists(p):
        saved = read_from_csv(sync_state, OBSOLETE_OBJECTS_FILE_KEY)
        keep = saved[~saved[FILE_NAME_KEY].isin(int_med[FILE_NAME_ON_DISK_KEY])]
        obsoletes = obsoletes.append(keep)

    obsoletes.drop_duplicates(inplace=True)
    save_to_csv(obsoletes, p)

    logger.info(f'Found {len(obsoletes.index)} obsolete files.')
    logger.info(f'Saving list to {p}')


def publish_new_manifest(int_med, sync_state):
    sample_table = int_med.pivot(
        index=SAMPLE_NAME_KEY,
        columns=[TYPE_KEY, READ_KEY],
        values=FILE_NAME_ON_DISK_KEY)

    # Multiindex approach ok, but this format needs changing
    # when dealing with FASTA in the same table
    sample_table.columns = [f"{seq_type}_R{read}".upper()
                            for (seq_type, read)
                            in sample_table.columns.to_flat_index()]
    sample_table.index.name = SEQ_ID_KEY
    sample_table.reset_index(inplace=True)
    m_path = os.path.join(sync_state[OUTPUT_DIR_KEY], sync_state[MANIFEST_KEY])

    save_to_csv(sample_table, m_path)
    logger.success(f'Published final manifest: {m_path}')


def get_file_from_server(df, index, row, sync_state):
    try:
        filename = row[FILE_NAME_ON_DISK_KEY]
        sample_name = row[SAMPLE_NAME_KEY]
        read = str(row[READ_KEY])
        seq_type = row[TYPE_KEY]
        sample_dir = os.path.join(sync_state[OUTPUT_DIR_KEY], sample_name)
        file_path = os.path.join(sample_dir, filename)

        query_path = _get_seq_download_path(
            sample_name,
            read,
            seq_type,
            BY_IS_ACTIVE_FLAG)

        if row[STATUS_KEY] == DRIFTED:
            fresh_name = f'{row[FILE_NAME_ON_DISK_KEY]}.fresh'
            logger.warning(f'Drifted from server: {file_path}. ')
            logger.info(f'Downloading fresh copy to temp file: {fresh_name}')

            df.at[index, HOT_SWAP_NAME_KEY] = fresh_name
            file_path = os.path.join(sample_dir, fresh_name)

        retry(lambda fp=file_path, fn=filename, qp=query_path, sd=sample_dir:
              _download_seq_file(file_path, filename, query_path, sample_dir),
              3,
              query_path)

        # Drifted entries are left for finalisation to hot swap.
        # Otherwise mark the entry as successfully downloaded.
        if df.at[index, STATUS_KEY] != DRIFTED:
            df.at[index, STATUS_KEY] = DOWNLOADED

    except Exception as ex:
        df.at[index, STATUS_KEY] = FAILED
        logger.error(f'Failed to download: {file_path}. Error: {ex}')


def set_match_status(df, index, row, seq_path):
    azure_path = os.path.join(row[BLOB_FILE_PATH_KEY], row[ORIGINAL_FILE_NAME_KEY])
    logger.success(f'Matched: {seq_path} ==> Azure: {azure_path}')
    df.at[index, STATUS_KEY] = MATCH


def analyse_status(df, do_hash_check, index, row, seq_path):
    previously_matched = row[STATUS_KEY] == MATCH

    if not os.path.exists(seq_path):
        logger.info(f'Missing: {seq_path}')
        df.at[index, STATUS_KEY] = MISSING

    elif do_hash_check and not previously_matched:
        file = open(seq_path, 'rb')
        seq_hash = hashlib.sha256(file.read()).hexdigest().lower()

        if seq_hash == row[SERVER_SHA_256_KEY].lower():
            set_match_status(df, index, row, seq_path)
        else:
            logger.info(f'Drifted: {seq_path}')
            df.at[index, STATUS_KEY] = DRIFTED

        file.close()

    else:
        # This happens in two cases:
        # 1) The user chose to not do hash checks.
        # 2) The entry was previously matched when the analysis
        #    got interrupted. Don't want to redo the hash checks
        #    again because the process could take hours. Just check
        #    that the file is still there.
        set_match_status(df, index, row, seq_path)
