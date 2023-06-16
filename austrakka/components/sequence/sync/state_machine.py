import os
import json
import hashlib
import pandas as pd
from loguru import logger

from .errors import StateMachineError
from ..funcs import _get_seq_data
from austrakka.utils.enums.seq import READ_BOTH
from austrakka.utils.enums.seq import BY_IS_ACTIVE_FLAG
from austrakka.components.sequence.funcs import _download_seq_file
from austrakka.components.sequence.funcs import _get_seq_download_path
from austrakka.utils.retry import retry

from .constant import MANIFEST_KEY
from .constant import INTERMEDIATE_MANIFEST_FILE_KEY
from .constant import GROUP_NAME_KEY
from .constant import SEQ_TYPE_KEY
from .constant import OUTPUT_DIR_KEY
from .constant import HASH_CHECK_KEY
from .constant import OBSOLETE_OBJECTS_FILE_KEY
from .constant import CURRENT_STATE_KEY
from .constant import CURRENT_ACTION_KEY
from .constant import SYNC_STATE_FILE_KEY
from .constant import SERVER_SHA_256_KEY

from .constant import FASTQ
from .constant import FASTA
from .constant import GZ

from .constant import FILE_NAME_KEY
from .constant import FILE_PATH_KEY
from .constant import SEQ_ID_KEY

from .constant import STATUS_KEY
from .constant import HOT_SWAP_NAME_KEY
from .constant import ORIGINAL_FILE_NAME_KEY
from .constant import BLOB_FILE_PATH_KEY
from .constant import SAMPLE_NAME_KEY
from .constant import FILE_NAME_ON_DISK_KEY
from .constant import READ_KEY
from .constant import TYPE_KEY

from .constant import DOWNLOADED
from .constant import DRIFTED
from .constant import FAILED
from .constant import MATCH
from .constant import MISSING
from .constant import DONE


class SName:
    PULLING_MANIFEST = 'PULLING_MANIFEST'
    DONE_PULLING_MANIFEST = 'DONE_PULLING_MANIFEST'
    ANALYSING = 'ANALYSING'
    DONE_ANALYSING = 'DONE_ANALYSING'
    DOWNLOADING = 'DOWNLOADING'
    DONE_DOWNLOADING = 'DONE_DOWNLOADING'
    FINALISING = 'FINALISING'
    DONE_FINALISING = 'DONE_FINALISING'
    FINALISATION_FAILED = 'FINALISATION_FAILED'
    PURGING = 'PURGING'
    DONE_PURGING = 'DONE_PURGING'
    UP_TO_DATE = 'UP_TO_DATE'


class Action:
    set_state_pulling_manifest = 'set-state/pulling-manifest'
    pull_manifest = 'pull-manifest'
    set_state_analysing = 'set-state/analysing'
    analyse = 'analyse'
    set_state_downloading = 'set-state/downloading'
    download = 'download'
    set_state_finalising = 'set-state/finalising'
    finalise = 'finalise'
    set_state_purging = 'set-state/purging'
    purge = 'purge'
    set_state_up_to_date = 'set-state/up-to-date'


class State:
    def __init__(
            self,
            name: str,
            is_end_state: bool = False,
            is_start_state: bool = False):

        self.name = name
        self.is_start_state = is_start_state
        self.is_end_state = is_end_state

    def is_valid(self):
        return self and self.name and not self.name.isspace()


class StateMachine:
    def __init__(self, states: dict[str, State], handlers: dict):
        self.action_handlers = handlers
        self.states: dict[str, State] = states
        self.actions: set[str] = set(handlers.keys())

    def run(self, sync_state: dict):
        if sync_state[CURRENT_STATE_KEY] not in self.states.keys():
            raise StateMachineError('The supplied current state is unknown '
                                    'to this state machine instance.')

        action = sync_state[CURRENT_ACTION_KEY]
        if action is None or action.isspace():
            raise StateMachineError(
                "Cannot set state. The current action is invalid. "
                "Accept only None or non-whitespace-only values.")

        if action not in self.actions:
            raise StateMachineError("The action is unknown to this state machine instance.")

        active_sync_state = sync_state.copy()
        current_state = self.states[active_sync_state[CURRENT_STATE_KEY]]

        logger.info('Start sync with args..')
        logger.info(f'{OUTPUT_DIR_KEY}: {sync_state[OUTPUT_DIR_KEY]}')
        logger.info(f'{GROUP_NAME_KEY}: {sync_state[GROUP_NAME_KEY]}')
        logger.info(f'{SEQ_TYPE_KEY}: {sync_state[SEQ_TYPE_KEY]}')
        logger.info(f'{HASH_CHECK_KEY}: {sync_state[HASH_CHECK_KEY]}')

        while not current_state.is_end_state:
            self.action_handlers[action](active_sync_state)

            path = os.path.join(
                active_sync_state[OUTPUT_DIR_KEY],
                active_sync_state[SYNC_STATE_FILE_KEY],
            )
            with open(path, 'w') as f:
                json.dump(active_sync_state, f)
                f.close()

            current_state = self.states[active_sync_state[CURRENT_STATE_KEY]]
            action = active_sync_state[CURRENT_ACTION_KEY]

    def get_state(self, name: str) -> State:
        return self.states[name]

    def is_known_state(self, name: str):
        return self.get_state(name) is not None

    def _ensure_is_known_state(self, s: State, msg: str):
        if not self.is_known_state(s.name):
            raise StateMachineError(msg)


def build_state_machine() -> StateMachine:
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
        }
    )


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
    do_hash_check = (HASH_CHECK_KEY not in sync_state) or\
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
    logger.info(f'Finished: {Action.analyse}')


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
    logger.info(f'Finished: {Action.download}')


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
        finalise_intermediate_manifest(int_med, sync_state)
        save_int_manifest(int_med, sync_state)
        save_final_manifest(int_med, sync_state)
        save_obsolete_files_list(int_med, sync_state)

        sync_state[CURRENT_STATE_KEY] = SName.DONE_FINALISING
        sync_state[CURRENT_ACTION_KEY] = Action.set_state_purging
        logger.info(f'Finished: {Action.finalise}')


def set_state_purging(sync_state: dict):
    sync_state[CURRENT_STATE_KEY] = SName.PURGING
    sync_state[CURRENT_ACTION_KEY] = Action.purge


def purge(sync_state: dict):
    logger.info(f'Started: {Action.purge}')
    sync_state[CURRENT_STATE_KEY] = SName.DONE_PURGING
    sync_state[CURRENT_ACTION_KEY] = Action.set_state_up_to_date
    logger.info(f'Finished: {Action.purge}')


def set_state_up_to_date(sync_state: dict):
    sync_state[CURRENT_STATE_KEY] = SName.UP_TO_DATE
    sync_state[CURRENT_ACTION_KEY] = Action.set_state_pulling_manifest


def get_path_from_state(sync_state: dict, key_to_file: str):
    path = os.path.join(
        sync_state[OUTPUT_DIR_KEY],
        sync_state[key_to_file],
    )
    return path


def read_from_csv(sync_state: dict, state_key: str):
    path = get_path_from_state(sync_state, state_key)
    df = pd.read_csv(path)
    return df


def save_int_manifest(df, sync_state):
    path = get_path_from_state(sync_state, INTERMEDIATE_MANIFEST_FILE_KEY)
    with open(path, 'w') as f:
        df.to_csv(f, index=False)
        f.close()


def save_to_csv(df, path):
    with open(path, 'w') as f:
        df.to_csv(f, index=False)
        f.close()


def finalise_intermediate_manifest(int_med, sync_state):
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

            logger.info(f'Hot swapped update for: {dest}')
            os.rename(src, dest)
            int_med.at[index, STATUS_KEY] = DONE

        elif int_med.at[index, STATUS_KEY] == MATCH or int_med.at[index, STATUS_KEY] == DOWNLOADED:
            int_med.at[index, STATUS_KEY] = DONE
            logger.success(f'Done: {dest}')

        else:
            raise StateMachineError('Reach an impossible state during finalise.'
                                    'Expecting only states "match", "downloaded", '
                                    'or "drifted"')


def save_obsolete_files_list(int_med, sync_state):
    logger.info('Checking for obsolete files..')

    # Get the list of files on disk. The array is a list of (full_path, file_name_only)
    files_on_disk = []
    obsoletes = pd.DataFrame({FILE_PATH_KEY: [], FILE_NAME_KEY: []})
    for (root_dir, dir_names, file_names) in os.walk(sync_state[OUTPUT_DIR_KEY]):
        for f in file_names:
            if os.path.splitext(f)[-1] in [FASTQ, FASTA, GZ]:
                files_on_disk.append((os.path.join(root_dir, f), f))

    # If files found on disk are not in the intermediate manifest,
    # it is added to the list of obsolete files.
    for tup in files_on_disk:
        r = int_med.loc[(int_med[FILE_NAME_ON_DISK_KEY] == tup[-1])]
        if len(r.index) == 0:
            obsoletes.loc[len(obsoletes.index)] = tup

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


def save_final_manifest(int_med, sync_state):
    sample_table = int_med.pivot(
        index=SAMPLE_NAME_KEY,
        columns=[TYPE_KEY, READ_KEY],
        values=FILE_NAME_ON_DISK_KEY)

    # Multiindex approach ok, but this format needs changing when dealing with FASTA in the same table
    sample_table.columns = [f"{seq_type}_R{read}".upper()
                            for (seq_type, read)
                            in sample_table.columns.to_flat_index()]
    sample_table.index.name = SEQ_ID_KEY
    sample_table.reset_index(inplace=True)
    m_path = os.path.join(sync_state[OUTPUT_DIR_KEY], sync_state[MANIFEST_KEY])

    logger.info(f'Saving final manifest: {m_path}')

    save_to_csv(sample_table, m_path)


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
            logger.warning(f'Drifted from server: {file_path}. Fixing..')
            fresh_name = f'{row[FILE_NAME_ON_DISK_KEY]}.fresh'
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
    if not os.path.exists(seq_path):
        logger.info(f'Missing: {seq_path}')
        df.at[index, STATUS_KEY] = MISSING
    elif do_hash_check:
        file = open(seq_path, 'rb')
        seq_hash = hashlib.sha256(file.read()).hexdigest().lower()
        if seq_hash == row[SERVER_SHA_256_KEY].lower():
            set_match_status(df, index, row, seq_path)
        else:
            logger.info(f'Drifted: {seq_path}')
            df.at[index, STATUS_KEY] = DRIFTED

        file.close()
    else:
        set_match_status(df, index, row, seq_path)
