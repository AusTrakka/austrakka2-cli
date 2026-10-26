from .constant import RESOURCE_NAME_KEY
from .constant import RESOURCE_TYPE_KEY
from .constant import SEQ_TYPE_KEY
from .constant import DOWNLOAD_BATCH_SIZE_KEY
from .constant import OUTPUT_DIR_KEY
from .errors import SyncError


def ensure_valid_state(sync_state):
    if RESOURCE_TYPE_KEY not in sync_state or RESOURCE_NAME_KEY not in sync_state:
        raise SyncError(
            f'{RESOURCE_TYPE_KEY} and {RESOURCE_NAME_KEY} were not both in state file.'
            'These specify the project or org previously synced here. We may be attempting to'
            'sync files from the wrong project or organisation. The sync state may be corrupt.'
        )

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

def ensure_resources_match(resource_value, resource_key, sync_state):
    if sync_state[resource_key] != resource_value:
        raise SyncError(
            f'{resource_key} in saved state: {sync_state[resource_key]} '
            f'differs from the parameter: {resource_value}. You are '
            f'probably about to override files from another '
            f'organisation or project. Aborting.')

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
