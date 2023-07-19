import os.path

from loguru import logger

from austrakka.utils.misc import logger_wraps
from austrakka.utils.fs import create_dir
from .sync_state import initialise, load_state
from .sync_workflow import select_start_state, configure_state_machine, reset

from .constant import SYNC_STATE_FILE
from .constant import OUTPUT_DIR_KEY
from .constant import SYNC_STATE_FILE_KEY
from .constant import CURRENT_STATE_KEY
from .constant import GROUP_NAME_KEY
from .constant import SEQ_TYPE_KEY
from .constant import RECALCULATE_HASH_KEY
from .constant import DOWNLOAD_BATCH_SIZE_KEY

from .sync_io import save_json


@logger_wraps()
def seq_get(
        output_dir: str,
        group_name: str,
        recalc_hash: bool,
        seq_type: str,
        download_batch_size: int,
        reset_opt: bool):

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

        # Settings allowed to be overriden between runs.
        sync_state[RECALCULATE_HASH_KEY] = recalc_hash
        sync_state[DOWNLOAD_BATCH_SIZE_KEY] = download_batch_size
        save_json(sync_state, state_file_path)

    elif not os.path.exists(output_dir):
        create_dir(output_dir)

    if CURRENT_STATE_KEY not in sync_state:
        sync_state = initialise(
            group_name,
            recalc_hash,
            output_dir,
            seq_type,
            download_batch_size)

        save_json(sync_state, state_file_path)

    if reset_opt:
        reset(state_file_path, sync_state)
    else:
        select_start_state(state_file_path, sync_state)

    logger.info('Starting sync with args..')
    logger.info(f'{OUTPUT_DIR_KEY}: {sync_state[OUTPUT_DIR_KEY]}')
    logger.info(f'{GROUP_NAME_KEY}: {sync_state[GROUP_NAME_KEY]}')
    logger.info(f'{SEQ_TYPE_KEY}: {sync_state[SEQ_TYPE_KEY]}')
    logger.info(f'{RECALCULATE_HASH_KEY}: {sync_state[RECALCULATE_HASH_KEY]}')

    state_machine = configure_state_machine()
    state_machine.run(sync_state)
    logger.success("Sync completed")
