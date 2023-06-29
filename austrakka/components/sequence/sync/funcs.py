import os.path

from loguru import logger

from austrakka.utils.misc import logger_wraps
from austrakka.utils.fs import create_dir
from .sync_state import initialise, set_to_start_state, load_state
from .sync_workflow import SName, configure_state_machine

from .constant import SYNC_STATE_FILE
from .constant import OUTPUT_DIR_KEY
from .constant import SYNC_STATE_FILE_KEY
from .constant import CURRENT_STATE_KEY
from .constant import GROUP_NAME_KEY
from .constant import SEQ_TYPE_KEY
from .constant import HASH_CHECK_KEY

from .sync_io import save_json


@logger_wraps()
def seq_get(output_dir: str, group_name: str, hash_check: bool, seq_type: str):

    sync_state = {}
    state_file_path = os.path.join(output_dir, SYNC_STATE_FILE)

    if os.path.exists(state_file_path):
        sync_state = load_state(
            group_name,
            output_dir,
            state_file_path,
            seq_type)

        # We just opened the file, so it has to be set to
        # the same file name for later use. It's probably
        # already the same thing. This will guarantee that.
        sync_state[SYNC_STATE_FILE_KEY] = SYNC_STATE_FILE

        # Hash check setting is allowed to be overriden between runs.
        sync_state[HASH_CHECK_KEY] = hash_check
        save_json(sync_state, state_file_path)

    elif not os.path.exists(output_dir):
        create_dir(output_dir)

    if CURRENT_STATE_KEY not in sync_state:
        sync_state = initialise(group_name, hash_check, output_dir, seq_type)
        save_json(sync_state, state_file_path)

    if sync_state[CURRENT_STATE_KEY] == SName.UP_TO_DATE:
        set_to_start_state(sync_state)
        save_json(sync_state, state_file_path)

    logger.info('Starting sync with args..')
    logger.info(f'{OUTPUT_DIR_KEY}: {sync_state[OUTPUT_DIR_KEY]}')
    logger.info(f'{GROUP_NAME_KEY}: {sync_state[GROUP_NAME_KEY]}')
    logger.info(f'{SEQ_TYPE_KEY}: {sync_state[SEQ_TYPE_KEY]}')
    logger.info(f'{HASH_CHECK_KEY}: {sync_state[HASH_CHECK_KEY]}')

    state_machine = configure_state_machine()
    state_machine.run(sync_state)
    logger.success("Sync completed")
