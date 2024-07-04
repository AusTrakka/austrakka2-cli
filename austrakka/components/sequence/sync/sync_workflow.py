# pylint: disable=broad-exception-caught
import os.path
from glob import glob
import re
from datetime import datetime
import shutil
import pandas as pd

from loguru import logger

from austrakka.components.sequence.funcs import _download_seq_file
from austrakka.components.sequence.funcs import _get_seq_download_path
from austrakka.utils.retry import retry
from austrakka.utils.enums.seq import SeqType

from .errors import WorkflowError
from .sync_io import \
    get_output_dir, \
    read_from_csv, \
    read_from_csv_or_empty, \
    get_path, \
    save_int_manifest, \
    calc_hash, \
    save_to_csv, \
    save_json

from .state_machine import StateMachine, SName, State, Action

from .constant import CURRENT_STATE_KEY, IS_ACTIVE_KEY
from .constant import CURRENT_ACTION_KEY
from .constant import RECALCULATE_HASH_KEY
from .constant import STATUS_KEY
from .constant import TRASH_DIR_KEY
from .constant import SAMPLE_NAME_KEY
from .constant import HOT_SWAP_NAME_KEY
from .constant import FILE_PATH_KEY
from .constant import DETECTION_DATE_KEY
from .constant import OBSOLETE_OBJECTS_FILE_KEY
from .constant import DOWNLOAD_BATCH_SIZE_KEY
from .constant import INTERMEDIATE_MANIFEST_FILE_KEY
from .constant import INTERMEDIATE_FASTA_AGGREGATE_FILE_NAME
from .constant import MANIFEST_KEY
from .constant import FASTA_AGGREGATE_FILE_NAME
from .constant import FILE_NAME_ON_DISK_KEY
from .constant import FILE_NAME_KEY
from .constant import INT_FILE_NAME_KEY
from .constant import SEQ_ID_KEY
from .constant import SEQ_TYPE_KEY
from .constant import TYPE_KEY
from .constant import READ_KEY
from .constant import GROUP_NAME_KEY
from .constant import BLOB_FILE_PATH_KEY
from .constant import SERVER_SHA_256_KEY

from .constant import MATCH
from .constant import DOWNLOADED
from .constant import DRIFTED
from .constant import FAILED
from .constant import DONE
from .constant import MISSING
from .constant import FASTA_EXTS
from .constant import FASTQ_EXTS
from .constant import GZ_EXT

from ..funcs import _get_seq_data

USE_CACHE = "use_cache"
CHECK_HASH = "check_hash"
DF = "df"
IDX = "idx"
ROW = "row"


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
        SName.AGGREGATING: State(SName.AGGREGATING),
        SName.DONE_AGGREGATING: State(SName.AGGREGATING),
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
        Action.set_state_aggregating: set_state_aggregating,
        Action.aggregate: aggregate,
        Action.set_state_purging: set_state_purging,
        Action.purge: purge,
        Action.set_state_up_to_date: set_state_up_to_date
    })


def set_state_aggregating(sync_state: dict):
    sync_state[CURRENT_STATE_KEY] = SName.AGGREGATING
    sync_state[CURRENT_ACTION_KEY] = Action.aggregate


def aggregate(sync_state: dict):
    logger.success(f'Started: {Action.aggregate}')

    if sync_state[SEQ_TYPE_KEY] != SeqType.FASTA_CNS.value:
        logger.info(f'No aggregation for {sync_state[SEQ_TYPE_KEY]}')
        sync_state[CURRENT_STATE_KEY] = SName.DONE_AGGREGATING
        sync_state[CURRENT_ACTION_KEY] = Action.set_state_purging
        logger.success(f'Finished: {Action.aggregate}')
        return

    p_man = read_from_csv(sync_state, MANIFEST_KEY)
    o_dir = get_output_dir(sync_state)
    int_all_fasta_path = os.path.join(o_dir, INTERMEDIATE_FASTA_AGGREGATE_FILE_NAME)

    with open(int_all_fasta_path, 'w', encoding='UTF-8') as int_aggr_file:
        logger.info(f'Aggregating {len(p_man.index)} fasta files.')
        logger.info(f'Generating {INTERMEDIATE_FASTA_AGGREGATE_FILE_NAME}..')
        for _, row in p_man.iterrows():
            header_key = manifest_column_key(FILE_NAME_ON_DISK_KEY, SeqType.FASTA_CNS.value)
            single_fasta_path = os.path.join(
                o_dir, row[SEQ_ID_KEY], SeqType.FASTA_CNS.value, row[header_key])
            if not os.path.exists(single_fasta_path):
                logger.error('Fasta file not found. Cannot aggregate '
                             'fasta files listed in the published manifest.')
                raise WorkflowError('Aggregate failed.')

            with open(single_fasta_path, 'r', encoding='UTF-8') as fasta:
                lines = fasta.readlines()
                int_aggr_file.writelines(lines)
                fasta.close()

        int_aggr_file.close()

    final_aggr_fasta_path = os.path.join(o_dir, FASTA_AGGREGATE_FILE_NAME)
    logger.info(f'Publishing {INTERMEDIATE_FASTA_AGGREGATE_FILE_NAME} to {final_aggr_fasta_path}')
    shutil.move(int_all_fasta_path, final_aggr_fasta_path)

    sync_state[CURRENT_STATE_KEY] = SName.DONE_AGGREGATING
    sync_state[CURRENT_ACTION_KEY] = Action.set_state_purging
    logger.success(f'Finished: {Action.aggregate}')


def set_state_pulling_manifest(sync_state: dict):
    sync_state[CURRENT_STATE_KEY] = SName.PULLING_MANIFEST
    sync_state[CURRENT_ACTION_KEY] = Action.pull_manifest


def pull_manifest(sync_state: dict):
    logger.success(f'Started: {Action.pull_manifest}')
    data = _get_seq_data(
        sync_state[SEQ_TYPE_KEY],
        sync_state[GROUP_NAME_KEY],
    )

    logger.success(f'Freshly pulled manifest has {len(data)} entries.')
    path = get_path(sync_state, INTERMEDIATE_MANIFEST_FILE_KEY)
    logger.info(f'Saving to intermediate manifest: {path}')

    if len(data) > 0:
        with open(path, 'w', encoding='UTF-8') as file:
            data.to_csv(file, index=False)
    else:
        initialise_empty_int_manifest(sync_state)

    sync_state[CURRENT_STATE_KEY] = SName.DONE_PULLING_MANIFEST
    sync_state[CURRENT_ACTION_KEY] = Action.set_state_analysing
    logger.success(f'Finished: {Action.pull_manifest}')


def set_state_analysing(sync_state: dict):
    sync_state[CURRENT_STATE_KEY] = SName.ANALYSING
    sync_state[CURRENT_ACTION_KEY] = Action.analyse


def analyse(sync_state: dict):
    logger.success(f'Started: {Action.analyse}')

    int_man = read_from_csv(sync_state, INTERMEDIATE_MANIFEST_FILE_KEY)
    published_manifest = read_from_csv_or_empty(sync_state, MANIFEST_KEY)

    if len(published_manifest.columns) == 0:
        published_manifest = initialise_empty_manifest(sync_state)

    use_hash_cache = not sync_state[RECALCULATE_HASH_KEY]

    ensure_valid(published_manifest, use_hash_cache, sync_state[SEQ_TYPE_KEY])

    if use_hash_cache:
        hash_cache = build_hash_dict(published_manifest)
    else:
        hash_cache = None

    if STATUS_KEY not in int_man.columns:
        int_man[STATUS_KEY] = ""

    output_dir = get_output_dir(sync_state)
    for index, row in int_man.iterrows():
        seq_path = os.path.join(
            output_dir,
            str(row[SAMPLE_NAME_KEY]),
            str(row[TYPE_KEY]),
            str(row[FILE_NAME_ON_DISK_KEY]))

        ctx = {DF: int_man, IDX: index, ROW: row}
        analyse_status(ctx, use_hash_cache, seq_path, hash_cache)

    save_int_manifest(int_man, sync_state)
    sync_state[CURRENT_STATE_KEY] = SName.DONE_ANALYSING
    sync_state[CURRENT_ACTION_KEY] = Action.set_state_downloading
    logger.success(f'Finished: {Action.analyse}')


def build_hash_dict(published_manifest):
    hash_dict = {}
    hash_keys = [c for c in published_manifest.columns if c.startswith('HASH_')]
    for _, row in published_manifest.iterrows():
        for hash_key in hash_keys:
            filename_key = hash_key[len('HASH_'):]
            hash_dict[row[filename_key]] = row[hash_key]
    return hash_dict


def ensure_valid(manifest, use_hash_cache, seq_type):
    """Check that the manifest contains the expected column headers"""

    if not use_hash_cache:
        return

    expected_headers = list_expected_headers(seq_type)

    if not set(manifest.columns) == set(expected_headers):
        raise WorkflowError(f"Cannot parse published manifest for seq type {seq_type}. "
                            f"Expected columns: {expected_headers}, "
                            f"found columns: {list(manifest.columns)}")


def set_state_downloading(sync_state: dict):
    sync_state[CURRENT_STATE_KEY] = SName.DOWNLOADING
    sync_state[CURRENT_ACTION_KEY] = Action.download


def download(sync_state: dict):
    logger.success(f'Started: {Action.download}')

    batch_size = sync_state[DOWNLOAD_BATCH_SIZE_KEY]
    data_frame = read_from_csv(sync_state, INTERMEDIATE_MANIFEST_FILE_KEY)

    if HOT_SWAP_NAME_KEY not in data_frame.columns:
        data_frame[HOT_SWAP_NAME_KEY] = ""

    save_int_manifest(data_frame, sync_state)

    path = get_path(sync_state, INTERMEDIATE_MANIFEST_FILE_KEY)
    with open(path, 'w', encoding='UTF-8') as file:
        for index, row in data_frame.iterrows():
            if row[STATUS_KEY] != DOWNLOADED and row[STATUS_KEY] != MATCH:
                get_file_from_server(data_frame, index, row, sync_state)

            if index % batch_size == 0:
                data_frame.to_csv(file, index=False)
                file.seek(0)

        # One final save.
        data_frame.to_csv(file, index=False)
        file.close()

    sync_state[CURRENT_STATE_KEY] = SName.DONE_DOWNLOADING
    sync_state[CURRENT_ACTION_KEY] = Action.set_state_finalising
    logger.success(f'Finished: {Action.download}')


def set_state_finalising(sync_state: dict):
    sync_state[CURRENT_STATE_KEY] = SName.FINALISING
    sync_state[CURRENT_ACTION_KEY] = Action.finalise


def finalise(sync_state: dict):
    logger.success(f'Started: {Action.finalise}')

    int_med = read_from_csv(sync_state, INTERMEDIATE_MANIFEST_FILE_KEY)
    errors = int_med.loc[(int_med[STATUS_KEY] != MATCH) &
                         (int_med[STATUS_KEY] != DOWNLOADED) &
                         (int_med[STATUS_KEY] != DRIFTED) &
                         (int_med[STATUS_KEY] != DONE)]

    if len(errors.index) > 0:
        im_path = get_path(sync_state, INTERMEDIATE_MANIFEST_FILE_KEY)

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
        sync_state[CURRENT_ACTION_KEY] = Action.set_state_aggregating
        logger.success(f'Finished: {Action.finalise}')


def set_state_purging(sync_state: dict):
    sync_state[CURRENT_STATE_KEY] = SName.PURGING
    sync_state[CURRENT_ACTION_KEY] = Action.purge


def purge(sync_state: dict):
    logger.success(f'Started: {Action.purge}')

    trash_dir_path = get_path(sync_state, TRASH_DIR_KEY)
    os.makedirs(trash_dir_path, exist_ok=True)

    output_dir = get_output_dir(sync_state)
    file_path = os.path.join(
        output_dir,
        sync_state[OBSOLETE_OBJECTS_FILE_KEY])

    move_delete_targets_to_trash(file_path, output_dir, trash_dir_path)

    # Remove the delete target file. It'll be recreated on the next run.
    os.remove(file_path)

    # Delete the intermediate manifest. It's no longer needed.
    # It'll be recreated on the next run.
    remove_int_manifest(output_dir, sync_state)

    sync_state[CURRENT_STATE_KEY] = SName.DONE_PURGING
    sync_state[CURRENT_ACTION_KEY] = Action.set_state_up_to_date
    logger.success(f'Finished: {Action.purge}')


def remove_int_manifest(output_dir, sync_state):
    int_m_path = os.path.join(
        output_dir,
        sync_state[INTERMEDIATE_MANIFEST_FILE_KEY])

    if os.path.exists(int_m_path):
        os.remove(int_m_path)


def set_state_up_to_date(sync_state: dict):
    sync_state[CURRENT_STATE_KEY] = SName.UP_TO_DATE
    sync_state[CURRENT_ACTION_KEY] = Action.set_state_pulling_manifest


def finalise_each_file(int_med, sync_state):
    output_dir = get_output_dir(sync_state)
    for index, row in int_med.iterrows():

        dest = os.path.join(
            output_dir,
            row[SAMPLE_NAME_KEY],
            row[TYPE_KEY],
            row[FILE_NAME_ON_DISK_KEY])

        if row[STATUS_KEY] == DRIFTED:
            src = os.path.join(
                output_dir,
                row[SAMPLE_NAME_KEY],
                row[TYPE_KEY],
                row[HOT_SWAP_NAME_KEY])

            logger.warning(f'Hot swapping: {dest}')
            os.rename(src, dest)
            logger.info(f'Done hot swapping: {dest}')

            int_med.at[index, STATUS_KEY] = DONE

        elif row[STATUS_KEY] == MATCH or\
                row[STATUS_KEY] == DOWNLOADED:

            int_med.at[index, STATUS_KEY] = DONE
            logger.info(f'Done: {dest}')

        elif row[STATUS_KEY] == DONE:
            logger.info(f'Already done: {dest}')

        else:
            raise WorkflowError(
                f'Reach an impossible state in the depths of {Action.finalise}. '
                f'Expecting each file state to be only "{MATCH}", '
                f'"{DOWNLOADED}", or "{DRIFTED}" but got something else. '
                f'The caller, probably {Action.finalise}, should have checked '
                f'my inputs before calling me.')

    logger.info(f'Finalized {int_med.shape[0]} entries.')
    save_int_manifest(int_med, sync_state)


def detect_and_record_obsolete_files(int_med, sync_state):
    logger.info('Checking for obsolete files..')

    # Get the list of files on disk. The array is a list of (full_path,
    # file_name_only)
    files_on_disk = []
    obsoletes = pd.DataFrame({
        FILE_PATH_KEY: [],
        FILE_NAME_KEY: [],
        DETECTION_DATE_KEY: []
    })

    # Subdirectories to scan are of form outdir/*/seqtype
    files = glob(os.path.join(get_output_dir(sync_state),'*',sync_state[SEQ_TYPE_KEY],'*'))

    seq_ext_regexstr = '|'.join(FASTQ_EXTS + FASTA_EXTS)
    seqfile_regex = re.compile(
        rf".+_[0-9TZ]+_[a-z0-9]{{8}}(_R\d)?(\.({seq_ext_regexstr}))?(\.({GZ_EXT}))?$")

    for path in files:
        if seqfile_regex.match(os.path.basename(path)):
            files_on_disk.append((
                path,
                os.path.basename(path),
                datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            ))
        else:
            logger.warning(
                f"Ignoring unexpected file {path} in sequence directory")

    # If files found on disk are not in the intermediate manifest,
    # it is added to the list of obsolete files.
    for triplet in files_on_disk:
        result = int_med.loc[(int_med[FILE_NAME_ON_DISK_KEY] == triplet[-2])]
        if len(result.index) == 0:
            obsoletes.loc[len(obsoletes.index)] = triplet

    # Check the reverse direction. If something is on the current obsolete list
    # of file, and is also in the intermediate manifest, then it needs to be
    # removed from the obsolete list. Additionally, if there is already an
    # entry on the obsolete list and still isn't on the intermediate manifest,
    # then it should be left on the obsolete list.
    path = get_path(sync_state, OBSOLETE_OBJECTS_FILE_KEY)
    if os.path.exists(path):
        saved = read_from_csv(sync_state, OBSOLETE_OBJECTS_FILE_KEY)
        keep = saved[~saved[FILE_NAME_KEY].isin(
            int_med[FILE_NAME_ON_DISK_KEY])]
        obsoletes = pd.concat([obsoletes,keep])

    obsoletes.drop_duplicates(
        subset=[
            FILE_PATH_KEY,
            FILE_NAME_KEY],
        inplace=True)
    save_to_csv(obsoletes, path)

    log_warn_or_success(
        len(obsoletes.index),
        f'Found {len(obsoletes.index)} obsolete files.'
    )
    logger.info(f'Saving list to {path}')


def log_warn_or_success(count, msg):
    if count > 0:
        logger.warning(msg)
    else:
        logger.success(msg)


def list_expected_headers(seq_type):
    reads = ['1', '2'] if seq_type == SeqType.FASTQ_ILL_PE.value else [None]
    expected_file_headers = [manifest_column_key(FILE_NAME_ON_DISK_KEY, seq_type, read)
                             for read in reads]
    expected_hash_headers = [manifest_column_key(SERVER_SHA_256_KEY, seq_type, read)
                             for read in reads]
    return [SEQ_ID_KEY] + expected_file_headers + expected_hash_headers


def list_default_int_manifest_headers():
    return [
        SEQ_ID_KEY,
        SAMPLE_NAME_KEY,
        INT_FILE_NAME_KEY,
        FILE_NAME_ON_DISK_KEY,
        BLOB_FILE_PATH_KEY,
        SERVER_SHA_256_KEY,
        TYPE_KEY,
        READ_KEY,
        IS_ACTIVE_KEY]


def initialise_empty_manifest(sync_state):
    default_headers = list_expected_headers(sync_state[SEQ_TYPE_KEY])
    published_manifest = pd.DataFrame(columns=default_headers)
    save_to_csv(published_manifest, get_path(sync_state, MANIFEST_KEY))
    return published_manifest


def initialise_empty_int_manifest(sync_state):
    default_headers = list_default_int_manifest_headers()
    int_man = pd.DataFrame(columns=default_headers)
    save_to_csv(int_man, get_path(sync_state, INTERMEDIATE_MANIFEST_FILE_KEY))
    return int_man


def publish_new_manifest(int_med, sync_state):
    sample_table = int_med.pivot(
        index=SAMPLE_NAME_KEY,
        columns=[TYPE_KEY, READ_KEY],
        values=[FILE_NAME_ON_DISK_KEY, SERVER_SHA_256_KEY])

    # Multiindex approach ok, but this format needs changing
    # when dealing with FASTA in the same table
    sample_table.columns = [manifest_column_key(file_or_hash, seq_type, read)
                            for (file_or_hash, seq_type, read)
                            in sample_table.columns.to_flat_index()]

    sample_table.index.name = SEQ_ID_KEY
    sample_table.reset_index(inplace=True)
    m_path = get_path(sync_state, MANIFEST_KEY)

    save_to_csv(sample_table, m_path)
    logger.success(f'Published final manifest: {m_path}')


def get_file_from_server(data_frame, index, row, sync_state):
    file_path = ""
    try:
        filename = row[FILE_NAME_ON_DISK_KEY]
        sample_name = row[SAMPLE_NAME_KEY]
        read = str(row[READ_KEY])
        seq_type = row[TYPE_KEY]
        dest_dir = os.path.join(get_output_dir(sync_state), sample_name, seq_type)
        file_path = os.path.join(dest_dir, filename)

        query_path, params = _get_seq_download_path(
            sample_name,
            read,
            seq_type,)

        if row[STATUS_KEY] == DRIFTED:
            fresh_name = f'{row[FILE_NAME_ON_DISK_KEY]}.fresh'
            logger.info(f'Drifted from server: {file_path}')
            logger.info(f'Downloading fresh copy to temp file: {fresh_name}')
            data_frame.at[index, HOT_SWAP_NAME_KEY] = fresh_name
            file_path = os.path.join(dest_dir, fresh_name)

        retry(lambda fp=file_path, fn=filename, qp=query_path, pm=params, sd=dest_dir:
              _download_seq_file(fp, fn, qp, pm, sd),
              1,
              query_path)

        check_download_hash(data_frame, file_path, index, row)

        # Drifted entries are left for finalisation to hot swap.
        # Otherwise mark the entry as successfully downloaded.
        if data_frame.at[index, STATUS_KEY] != DRIFTED and \
                data_frame.at[index, STATUS_KEY] != FAILED:

            data_frame.at[index, STATUS_KEY] = DOWNLOADED

    except Exception as ex:
        data_frame.at[index, STATUS_KEY] = FAILED
        logger.error(f'Failed to download: {file_path}. Error: {ex}')


def check_download_hash(data_frame, file_path, index, row):
    local_hash = calc_hash(file_path)
    server_hash = row[SERVER_SHA_256_KEY]

    if local_hash.casefold() != server_hash.casefold():
        logger.error(f"Bad hash. Invalidating: {file_path}")
        data_frame.at[index, STATUS_KEY] = FAILED


def set_match_status(ctx, seq_path):
    azure_path = os.path.join(
        ctx[ROW][BLOB_FILE_PATH_KEY],
        ctx[ROW][INT_FILE_NAME_KEY])
    logger.info(f'Matched: {seq_path} ==> Azure: {azure_path}')
    ctx[DF].at[ctx[IDX], STATUS_KEY] = MATCH


def analyse_status(
        ctx: dict,
        use_hash_cache: bool,
        seq_path: str,
        hash_cache: dict):
    previously_matched = ctx[ROW][STATUS_KEY] == MATCH

    if not os.path.exists(seq_path):
        logger.warning(f'Missing: {seq_path}')
        ctx[DF].at[ctx[IDX], STATUS_KEY] = MISSING

    elif (not previously_matched) or ctx[ROW][STATUS_KEY] == FAILED:

        # If told to use cache and there is a cache hit.
        if use_hash_cache and ctx[ROW][FILE_NAME_ON_DISK_KEY] in hash_cache:
            logger.info("Hash cache hit.")
            seq_hash = hash_cache[ctx[ROW][FILE_NAME_ON_DISK_KEY]]
        else:
            seq_hash = calc_hash(seq_path)

        if seq_hash.casefold() == ctx[ROW][SERVER_SHA_256_KEY].casefold():
            set_match_status(ctx, seq_path)
        else:
            logger.warning(f'Drifted: {seq_path}')
            ctx[DF].at[ctx[IDX], STATUS_KEY] = DRIFTED

    else:
        # This happens in two cases:
        # 1) The user chose to not do hash checks.
        # 2) The entry was previously matched when the analysis
        #    got interrupted. Don't want to redo the hash checks
        #    again because the process could take hours. Just check
        #    that the file is still there.
        set_match_status(ctx, seq_path)


def move_delete_targets_to_trash(
        obsolete_objects_file_path,
        output_dir,
        trash_dir_path):

    trash = pd.read_csv(obsolete_objects_file_path)

    log_warn_or_success(
        len(trash.index),
        f'Found: {len(trash.index)} files to purge.'
    )

    for _, row in trash.iterrows():
        if os.path.exists(row[FILE_PATH_KEY]):

            # Get the file's parent directories not including output_dir
            dest_dir = mirror_parent_sub_dirs(output_dir, row, trash_dir_path)
            dest_file = os.path.join(dest_dir, row[FILE_NAME_KEY])
            logger.warning(
                f'Moving to trash: {row[FILE_PATH_KEY]} ==> {dest_file}')
            shutil.move(row[FILE_PATH_KEY], dest_file)

            # Clean up parent (seq type) directory, and grandparent (sample) directory if empty
            # Note a parallel process for a different seq type could create a race condition
            src_dir = os.path.dirname(row[FILE_PATH_KEY])
            if len(os.listdir(src_dir)) == 0:
                logger.info(f"Removing empty directory: {src_dir}")
                os.rmdir(src_dir)
                sample_dir = os.path.dirname(src_dir)
                if len(os.listdir(sample_dir)) == 0:
                    logger.info(f"Removing empty directory: {sample_dir}")
                    os.rmdir(sample_dir)


def mirror_parent_sub_dirs(output_dir, row, trash_dir_path):
    sub_paths = os.path.dirname(row[FILE_PATH_KEY]).removeprefix(output_dir)
    if sub_paths.startswith('/'):
        sub_paths = sub_paths[1:]

    # Make the destination directory structure
    dest_dir = os.path.join(trash_dir_path, sub_paths)
    os.makedirs(dest_dir, exist_ok=True)
    return dest_dir


def select_start_state(state_file_path, sync_state):
    if sync_state[CURRENT_STATE_KEY] == SName.UP_TO_DATE:
        set_state_pulling_manifest(sync_state)
        save_json(sync_state, state_file_path)

    elif sync_state[CURRENT_STATE_KEY] == SName.FINALISATION_FAILED:
        set_state_analysing(sync_state)
        save_json(sync_state, state_file_path)


def reset(state_file_path, sync_state):
    output_dir = get_output_dir(sync_state)
    remove_int_manifest(output_dir, sync_state)
    set_state_pulling_manifest(sync_state)
    save_json(sync_state, state_file_path)


def manifest_column_key(file_or_hash: str, seq_type: str, read:str = None):
    """Define desired column header for the manifest file"""
    assert file_or_hash in [FILE_NAME_ON_DISK_KEY, SERVER_SHA_256_KEY]
    header = (("HASH_" if file_or_hash==SERVER_SHA_256_KEY else "") + 
              seq_type.upper().replace('_','-'))
    if seq_type==SeqType.FASTQ_ILL_PE.value:
        assert read is not None
        header += f"_R{read}"
    return header
