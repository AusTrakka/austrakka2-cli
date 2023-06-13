import json
import os
from typing import Dict
from austrakka.utils.misc import logger_wraps
from austrakka.utils.fs import create_dir
from .state_machine import build_state_machine, SName, Action

MANIFEST_FILE_NAME = 'manifest.csv'
INTERMEDIATE_MANIFEST_FILE = 'intermediate-manifest.csv'
OBSOLETE_OBJECTS_FILE = 'obsolete-objects.json'
SYNC_STATE_FILE = 'sync-state.json'
FASTQ = 'fastq'


@logger_wraps()
def fastq_sync(output_dir: str, group_name: str):

    sync_state = dict()
    state_file_path = os.path.join(output_dir, SYNC_STATE_FILE)

    if os.path.exists(output_dir):
        sync_state = read_sync_state(state_file_path)
    else:
        create_dir(output_dir)

    if "current_state" not in sync_state:
        set_to_start_state(sync_state)
        sync_state["sync_state_file"] = SYNC_STATE_FILE
        sync_state["manifest"] = MANIFEST_FILE_NAME
        sync_state["obsolete_objects_file"] = OBSOLETE_OBJECTS_FILE
        sync_state["intermediate_manifest_file"] = INTERMEDIATE_MANIFEST_FILE
        sync_state["group_name"] = group_name
        sync_state["seq_type"] = FASTQ
        sync_state["output_dir"] = output_dir
        save_json(sync_state, state_file_path)

    if sync_state['current_state'] == SName.UP_TO_DATE:
        set_to_start_state(sync_state)
        save_json(sync_state, state_file_path)

    sm = build_state_machine()
    sm.run(sync_state)
    print("done")


def set_to_start_state(sync_state):
    sync_state["current_state"] = SName.PULLING_MANIFEST
    sync_state["current_action"] = Action.pull_manifest


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
