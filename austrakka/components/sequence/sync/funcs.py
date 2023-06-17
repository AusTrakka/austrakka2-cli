import os.path

from austrakka.utils.misc import logger_wraps
from austrakka.utils.fs import create_dir
from .sync_workflow import *
from .sync_validator import *
from .constant import *


@logger_wraps()
def fastq_sync(output_dir: str, group_name: str, hash_check: bool):

    sync_state = dict()
    state_file_path = os.path.join(output_dir, SYNC_STATE_FILE)

    if os.path.exists(state_file_path):
        sync_state = read_sync_state(state_file_path)
        ensure_valid_state(sync_state)
        ensure_group_names_match(group_name, sync_state)
        ensure_output_dir_match(output_dir, sync_state)
        ensure_is_present(
            sync_state,
            TRASH_DIR_KEY,
            "No trash directory found in the current state file. "
            "The state file might be corrupt. Ask an admin for help")

        # We just opened the file, so it has to be set to
        # the same file name for later use. It's probably
        # already the same thing. This will guarantee that.
        sync_state[SYNC_STATE_FILE_KEY] = SYNC_STATE_FILE
        save_json(sync_state, state_file_path)
    elif not os.path.exists(output_dir):
        create_dir(output_dir)

    if CURRENT_STATE_KEY not in sync_state:
        trash = os.path.join(output_dir, TRASH_DIR)

        set_to_start_state(sync_state)
        sync_state[SYNC_STATE_FILE_KEY] = SYNC_STATE_FILE
        sync_state[MANIFEST_KEY] = MANIFEST_FILE_NAME
        sync_state[OBSOLETE_OBJECTS_FILE_KEY] = OBSOLETE_OBJECTS_FILE
        sync_state[INTERMEDIATE_MANIFEST_FILE_KEY] = INTERMEDIATE_MANIFEST_FILE
        sync_state[GROUP_NAME_KEY] = group_name
        sync_state[SEQ_TYPE_KEY] = FASTQ
        sync_state[HASH_CHECK_KEY] = hash_check
        sync_state[OUTPUT_DIR_KEY] = output_dir
        sync_state[TRASH_DIR_KEY] = trash
        save_json(sync_state, state_file_path)

    if sync_state[CURRENT_STATE_KEY] == SName.UP_TO_DATE:
        set_to_start_state(sync_state)
        save_json(sync_state, state_file_path)

    logger.info('Starting sync with args..')
    logger.info(f'{OUTPUT_DIR_KEY}: {sync_state[OUTPUT_DIR_KEY]}')
    logger.info(f'{GROUP_NAME_KEY}: {sync_state[GROUP_NAME_KEY]}')
    logger.info(f'{SEQ_TYPE_KEY}: {sync_state[SEQ_TYPE_KEY]}')
    logger.info(f'{HASH_CHECK_KEY}: {sync_state[HASH_CHECK_KEY]}')

    sm = configure_state_machine()
    sm.run(sync_state)
    logger.success("Sync completed")


def set_if_not_present(sync_state):
    if SYNC_STATE_FILE_KEY not in sync_state:
        sync_state[SYNC_STATE_FILE_KEY] = SYNC_STATE_FILE


def set_to_start_state(sync_state):
    sync_state[CURRENT_STATE_KEY] = SName.PULLING_MANIFEST
    sync_state[CURRENT_ACTION_KEY] = Action.pull_manifest
