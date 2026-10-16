import sys
import os.path

from loguru import logger

from trakka.utils.misc import logger_wraps
from trakka.utils.fs import create_dir
from .sync_state import initialise, load_state
from .sync_workflow import select_start_state, configure_state_machine, reset
from .sync_io import save_json

from .constant import SYNC_STATE_FILE
from .constant import OUTPUT_DIR_KEY
from .constant import CURRENT_STATE_KEY
from .constant import RESOURCE_NAME_KEY, RESOURCE_TYPE_KEY
from .constant import RT_PROJECT, RT_ORG
from .constant import SEQ_TYPE_KEY
from .constant import RECALCULATE_HASH_KEY
from .constant import DOWNLOAD_BATCH_SIZE_KEY
from .constant import SYNC_STATE_FILE_KEY


@logger_wraps()
def seq_sync_get(
        output_dir: str,
        project: str,
        org: str,
        recalc_hash: bool,
        seq_type: str,
        download_batch_size: int,
        reset_opt: bool):

    sync_state = {}
    state_file_path = os.path.join(output_dir, SYNC_STATE_FILE.replace('SEQTYPE', seq_type))

    resource_type = None
    resource_name = None
    if project is not None:
        resource_type = RT_PROJECT
        resource_name = project
    elif org is not None:
        resource_type = RT_ORG
        resource_name = org
    if resource_type is None or resource_name is None:
        # Should in theory have been prevented by click
        raise ValueError("Project and organisation values were both empty")

    if os.path.exists(state_file_path):
        sync_state = load_state(
            resource_type,
            resource_name,
            output_dir,
            state_file_path,
            seq_type)

        # We just opened the file, so it has to be set to
        # the same file name for later use. It's probably
        # already the same thing. This will guarantee that.
        sync_state[SYNC_STATE_FILE_KEY] = SYNC_STATE_FILE.replace('SEQTYPE', seq_type)

        # Settings allowed to be overriden between runs.
        sync_state[RECALCULATE_HASH_KEY] = recalc_hash
        sync_state[DOWNLOAD_BATCH_SIZE_KEY] = download_batch_size
        save_json(sync_state, state_file_path)

    elif not os.path.exists(output_dir):
        create_dir(output_dir)

    if CURRENT_STATE_KEY not in sync_state:
        sync_state = initialise(
            resource_type,
            resource_name,
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
    logger.info(f'{RESOURCE_TYPE_KEY}: {sync_state[RESOURCE_TYPE_KEY]}')
    logger.info(f'{RESOURCE_NAME_KEY}: {sync_state[RESOURCE_NAME_KEY]}')
    logger.info(f'{SEQ_TYPE_KEY}: {sync_state[SEQ_TYPE_KEY]}')
    logger.info(f'{RECALCULATE_HASH_KEY}: {sync_state[RECALCULATE_HASH_KEY]}')

    state_machine = configure_state_machine()
    final_state = state_machine.run(sync_state)
    # Should not be necessary to check final_state.is_end_state since this must happen unless
    #  an exception was thrown, in which case we don't get here.
    # However check final_state.is_error_state
    if final_state.is_error_state:
        logger.error("Sync ended in error state.")
        sys.exit(1)
    else:
        logger.success("Sync completed.")
