from .sync_workflow import SName, Action
from .sync_validator import \
    ensure_valid_state, \
    ensure_group_names_match, \
    ensure_output_dir_match, \
    ensure_seq_type_matches, \
    ensure_is_present

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
from .constant import CURRENT_STATE_KEY
from .constant import CURRENT_ACTION_KEY
from .constant import GROUP_NAME_KEY
from .constant import SEQ_TYPE_KEY
from .constant import HASH_CHECK_KEY

from .sync_io import read_sync_state


def initialise(group_name, hash_check, output_dir, seq_type) -> dict:
    sync_state = {}
    set_to_start_state(sync_state)
    sync_state[SYNC_STATE_FILE_KEY] = SYNC_STATE_FILE
    sync_state[MANIFEST_KEY] = MANIFEST_FILE_NAME
    sync_state[OBSOLETE_OBJECTS_FILE_KEY] = OBSOLETE_OBJECTS_FILE
    sync_state[INTERMEDIATE_MANIFEST_FILE_KEY] = INTERMEDIATE_MANIFEST_FILE
    sync_state[SEQ_TYPE_KEY] = seq_type
    sync_state[GROUP_NAME_KEY] = group_name
    sync_state[HASH_CHECK_KEY] = hash_check
    sync_state[OUTPUT_DIR_KEY] = output_dir
    sync_state[TRASH_DIR_KEY] = TRASH_DIR
    return sync_state


def load_state(group_name, output_dir, state_file_path, seq_type):
    sync_state = read_sync_state(state_file_path)
    ensure_valid_state(sync_state)
    ensure_group_names_match(group_name, sync_state)
    ensure_output_dir_match(output_dir, sync_state)
    ensure_seq_type_matches(seq_type, sync_state)
    ensure_is_present(
        sync_state,
        TRASH_DIR_KEY,
        "No trash directory found in the current state file. "
        "The state file might be corrupt. Ask an admin for help")

    return sync_state


def set_to_start_state(sync_state):
    sync_state[CURRENT_STATE_KEY] = SName.PULLING_MANIFEST
    sync_state[CURRENT_ACTION_KEY] = Action.pull_manifest
