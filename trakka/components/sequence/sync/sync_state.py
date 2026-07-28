from .sync_validator import \
    ensure_valid_state, \
    ensure_group_names_match, \
    ensure_output_dir_match, \
    ensure_seq_type_matches, \
    ensure_is_present, \
    ensure_download_batch_size_positive

from .constant import SYNC_STATE_FILE
from .constant import INTERMEDIATE_MANIFEST_FILE
from .constant import MANIFEST_FILE_NAME
from .constant import OBSOLETE_OBJECTS_FILE
from .constant import TRASH_DIR
from .constant import TRASH_DIR_KEY
from .constant import OUTPUT_DIR_KEY
from .constant import INTERMEDIATE_MANIFEST_FILE_KEY
from .constant import SYNC_STATE_FILE_KEY
from .constant import MANIFEST_KEY
from .constant import OBSOLETE_OBJECTS_FILE_KEY
from .constant import GROUP_NAME_KEY
from .constant import SEQ_TYPE_KEY
from .constant import RECALCULATE_HASH_KEY
from .constant import DOWNLOAD_BATCH_SIZE_KEY

from .sync_io import read_sync_state
from .sync_workflow import set_state_pulling_manifest


def initialise(
        group_name,
        recalc_hash,
        output_dir,
        seq_type,
        download_batch_size) -> dict:
    sync_state = {}
    set_state_pulling_manifest(sync_state)
    sync_state[SYNC_STATE_FILE_KEY] = SYNC_STATE_FILE.replace('SEQTYPE', seq_type)
    sync_state[MANIFEST_KEY] = MANIFEST_FILE_NAME.replace('SEQTYPE', seq_type)
    sync_state[OBSOLETE_OBJECTS_FILE_KEY] = OBSOLETE_OBJECTS_FILE.replace('SEQTYPE', seq_type)
    sync_state[INTERMEDIATE_MANIFEST_FILE_KEY] = \
        INTERMEDIATE_MANIFEST_FILE.replace('SEQTYPE', seq_type)
    sync_state[SEQ_TYPE_KEY] = seq_type
    sync_state[GROUP_NAME_KEY] = group_name
    sync_state[RECALCULATE_HASH_KEY] = recalc_hash
    sync_state[OUTPUT_DIR_KEY] = output_dir
    sync_state[TRASH_DIR_KEY] = TRASH_DIR
    sync_state[DOWNLOAD_BATCH_SIZE_KEY] = download_batch_size
    return sync_state


def load_state(group_name, output_dir, state_file_path, seq_type):
    sync_state = read_sync_state(state_file_path)
    ensure_valid_state(sync_state)
    ensure_group_names_match(group_name, sync_state)
    ensure_output_dir_match(output_dir, sync_state)
    ensure_seq_type_matches(seq_type, sync_state)
    ensure_download_batch_size_positive(sync_state[DOWNLOAD_BATCH_SIZE_KEY])
    ensure_is_present(
        sync_state,
        TRASH_DIR_KEY,
        "No trash directory found in the current state file. "
        "The state file might be corrupt. Ask an admin for help")

    return sync_state

# Used for migration from old sync system. Does not attempt to enforce group or type
def load_old_state(output_dir, state_file_path):
    sync_state = read_sync_state(state_file_path)
    ensure_valid_state(sync_state)
    ensure_output_dir_match(output_dir, sync_state)
    ensure_download_batch_size_positive(sync_state[DOWNLOAD_BATCH_SIZE_KEY])
    ensure_is_present(
        sync_state,
        TRASH_DIR_KEY,
        "No trash directory found in the current state file. "
        "The state file might be corrupt. Ask an admin for help")

    return sync_state
