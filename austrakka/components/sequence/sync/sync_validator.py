from .constant import GROUP_NAME_KEY
from .constant import SEQ_TYPE_KEY
from .constant import DOWNLOAD_BATCH_SIZE_KEY
from .constant import OUTPUT_DIR_KEY
from .errors import SyncError


def ensure_valid_state(sync_state):
    ensure_is_present(
        sync_state,
        GROUP_NAME_KEY,
        f'{GROUP_NAME_KEY} is not found in state. '
        'Beware, you could be clobbering files for another group.')

    ensure_is_present(
        sync_state,
        OUTPUT_DIR_KEY,
        f'{OUTPUT_DIR_KEY} is not found in state. '
        'It should have been saved from a previous run. Is the state'
        'file corrupt? Check your output directory and perhaps delete'
        'sync-state.json before continuing.')

    ensure_is_present(
        sync_state,
        SEQ_TYPE_KEY,
        f'{SEQ_TYPE_KEY} is not found in state. '
        'It should have been saved from a previous run. Is the state '
        'file corrupt? Check your output directory and perhaps delete '
        'sync-state.json before continuing.')


def ensure_seq_type_matches(seq_type, sync_state):
    if sync_state[SEQ_TYPE_KEY] != seq_type:
        raise SyncError(
            f'{SEQ_TYPE_KEY} in saved state: "{sync_state[SEQ_TYPE_KEY]}" '
            f'differs from the parameter: "{seq_type}". Is the state '
            'file corrupt? Check your output directory and perhaps delete '
            'sync-state.json before continuing.')


def ensure_group_names_match(group_name, sync_state):
    if sync_state[GROUP_NAME_KEY] != group_name:
        raise SyncError(
            f'{GROUP_NAME_KEY} in saved state: {sync_state[GROUP_NAME_KEY]} '
            f'differs from the parameter: {group_name}. You are '
            f'probably about to override files from another '
            f'group or project. This is not allowed.')


def ensure_download_batch_size_positive(download_batch_size):
    if download_batch_size < 1:
        raise SyncError(f'{DOWNLOAD_BATCH_SIZE_KEY} must be greater than 0.')


def ensure_is_present(sync_state, key, msg):
    if key not in sync_state:
        raise SyncError(msg)


def ensure_output_dir_match(path, sync_state):
    if sync_state[OUTPUT_DIR_KEY] != path:
        raise SyncError(
            f'{OUTPUT_DIR_KEY} in saved state: {sync_state[OUTPUT_DIR_KEY]} '
            f'differs from the parameter: {path}, but you obviously found '
            f'this file via the path. Your state file might be corrupt. '
            f'Your options are: 1) correct the parameters in the state file. '
            f'2) delete the state file - this will be destructive. 3) '
            f'start a fresh sync to a different folder.')
