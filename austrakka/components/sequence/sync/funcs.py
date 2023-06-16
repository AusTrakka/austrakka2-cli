import json
import os
from loguru import logger
from typing import Dict
from austrakka.utils.misc import logger_wraps
from austrakka.utils.fs import create_dir
from .state_machine import build_state_machine, SName, Action
from .sync_validator import ensure_valid_state
from .sync_validator import ensure_group_names_match
from .sync_validator import ensure_output_dir_match
from .constant import SYNC_STATE_FILE_KEY
from .constant import MANIFEST_KEY
from .constant import INTERMEDIATE_MANIFEST_FILE_KEY
from .constant import GROUP_NAME_KEY
from .constant import SEQ_TYPE_KEY
from .constant import OUTPUT_DIR_KEY
from .constant import HASH_CHECK_KEY
from .constant import OBSOLETE_OBJECTS_FILE_KEY
from .constant import CURRENT_STATE_KEY
from .constant import CURRENT_ACTION_KEY

MANIFEST_FILE_NAME = 'manifest.csv'
INTERMEDIATE_MANIFEST_FILE = 'intermediate-manifest.csv'
OBSOLETE_OBJECTS_FILE = 'delete-targets.csv'
SYNC_STATE_FILE = 'sync-state.json'
FASTQ = 'fastq'


@logger_wraps()
def fastq_sync(output_dir: str, group_name: str, hash_check: bool):

    sync_state = dict()
    state_file_path = os.path.join(output_dir, SYNC_STATE_FILE)

    if os.path.exists(state_file_path):
        sync_state = read_sync_state(state_file_path)
        ensure_valid_state(sync_state)
        ensure_group_names_match(group_name, sync_state)
        ensure_output_dir_match(output_dir, sync_state)

        # We just opened the file, so it has to be set to
        # the same file name for later use. It's probably
        # already the same thing. This will guarantee that.
        sync_state[SYNC_STATE_FILE_KEY] = SYNC_STATE_FILE
        save_json(sync_state, state_file_path)
    elif not os.path.exists(output_dir):
        create_dir(output_dir)

    if CURRENT_STATE_KEY not in sync_state:
        set_to_start_state(sync_state)
        sync_state[SYNC_STATE_FILE_KEY] = SYNC_STATE_FILE
        sync_state[MANIFEST_KEY] = MANIFEST_FILE_NAME
        sync_state[OBSOLETE_OBJECTS_FILE_KEY] = OBSOLETE_OBJECTS_FILE
        sync_state[INTERMEDIATE_MANIFEST_FILE_KEY] = INTERMEDIATE_MANIFEST_FILE
        sync_state[GROUP_NAME_KEY] = group_name
        sync_state[SEQ_TYPE_KEY] = FASTQ
        sync_state[HASH_CHECK_KEY] = hash_check
        sync_state[OUTPUT_DIR_KEY] = output_dir
        save_json(sync_state, state_file_path)

    if sync_state[CURRENT_STATE_KEY] == SName.UP_TO_DATE:
        set_to_start_state(sync_state)
        save_json(sync_state, state_file_path)

    sm = build_state_machine()
    sm.run(sync_state)
    logger.info("Sync completed")


def set_if_not_in(sync_state):
    if SYNC_STATE_FILE_KEY not in sync_state:
        sync_state[SYNC_STATE_FILE_KEY] = SYNC_STATE_FILE


def set_to_start_state(sync_state):
    sync_state[CURRENT_STATE_KEY] = SName.PULLING_MANIFEST
    sync_state[CURRENT_ACTION_KEY] = Action.pull_manifest


def save_json(dict_obj: Dict, path: str):
    with open(path, 'w') as f:
        json.dump(dict_obj, f)


def read_sync_state(path: str) -> Dict:
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    else:
        return {}


class SyncError(Exception):
    pass
