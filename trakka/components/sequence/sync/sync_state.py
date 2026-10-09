from loguru import logger

from .sync_validator import \
    ensure_valid_state, \
    ensure_resources_match, \
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
from .constant import RESOURCE_NAME_KEY
from .constant import RESOURCE_TYPE_KEY
from .constant import SEQ_TYPE_KEY
from .constant import RECALCULATE_HASH_KEY
from .constant import DOWNLOAD_BATCH_SIZE_KEY

from .constant import RT_PROJECT, RT_ORG

from .sync_io import read_sync_state
from .sync_workflow import set_state_pulling_manifest


def initialise(
# pylint: disable=R0801
        resource_type,
        resource_name,
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
    sync_state[RESOURCE_TYPE_KEY] = resource_type
    sync_state[RESOURCE_NAME_KEY] = resource_name
    sync_state[RECALCULATE_HASH_KEY] = recalc_hash
    sync_state[OUTPUT_DIR_KEY] = output_dir
    sync_state[TRASH_DIR_KEY] = TRASH_DIR
    sync_state[DOWNLOAD_BATCH_SIZE_KEY] = download_batch_size
    return sync_state


def load_state(resource_type, resource_name, output_dir, state_file_path, seq_type):
    sync_state = read_sync_state(state_file_path)
    if GROUP_NAME_KEY in sync_state:
        _handle_legacy_state(sync_state)
    ensure_valid_state(sync_state)
    ensure_resources_match(resource_type, RESOURCE_TYPE_KEY, sync_state)
    ensure_resources_match(resource_name, RESOURCE_NAME_KEY, sync_state)
    ensure_output_dir_match(output_dir, sync_state)
    ensure_seq_type_matches(seq_type, sync_state)
    ensure_download_batch_size_positive(sync_state[DOWNLOAD_BATCH_SIZE_KEY])
    ensure_is_present(
        sync_state,
        TRASH_DIR_KEY,
        "No trash directory found in the current state file. "
        "The state file might be corrupt. Ask an admin for help")

    return sync_state

def _handle_legacy_state(sync_state):
    """
    Convert group_name to resource_type and resource_name.
    Updates sync_state in place.
    """
    logger.info("Detected legacy state file, updating state")
    group_name = sync_state[GROUP_NAME_KEY]
    group_prefix = '-'.join(group_name.split('-')[:-1])
    group_suffix = group_name.split('-')[-1]
    if group_suffix == "Owner":
        sync_state[RESOURCE_TYPE_KEY] = RT_ORG
    elif group_suffix == "Group":
        sync_state[RESOURCE_TYPE_KEY] = RT_PROJECT
    else:
        raise ValueError(f"Cannot parse group {group_name} as a project or organisation group")
    sync_state[RESOURCE_NAME_KEY] = group_prefix
    del sync_state[GROUP_NAME_KEY]
    logger.info(f"Updated group {group_name}"
                + " to {sync_state[RESOURCE_TYPE_KEY]} {sync_state[RESOURCE_NAME_KEY]}")
