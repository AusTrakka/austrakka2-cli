import os
import json
import pandas as pd

from .constant import *
from .errors import SyncError

invalid_output_dir = [
    '/', '/usr', '/home', '/bin', '/sbin', '/var', '/etc', '/opt'
]


def save_json(dict_obj: dict, path: str):
    with open(path, 'w') as f:
        json.dump(dict_obj, f)


def read_sync_state(path: str) -> dict:
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    else:
        return {}


def read_from_csv(sync_state: dict, state_key: str):
    path = get_path(sync_state, state_key)
    df = pd.read_csv(path)
    return df


def save_int_manifest(df, sync_state):
    path = get_path(sync_state, INTERMEDIATE_MANIFEST_FILE_KEY)
    with open(path, 'w') as f:
        df.to_csv(f, index=False)
        f.close()


def save_to_csv(df, path):
    with open(path, 'w') as f:
        df.to_csv(f, index=False)
        f.close()


def get_path(sync_state: dict, key_to_file: str):
    path = os.path.join(
        get_output_dir(sync_state),
        sync_state[key_to_file],
    )
    return path


def get_output_dir(sync_state):
    output_dir = sync_state[OUTPUT_DIR_KEY]
    if output_dir in invalid_output_dir or f'{output_dir}/' in invalid_output_dir:
        raise SyncError("Found invalid output directory path while "
                        "building trash directory path. You should not be "
                        f"sending data to a system folder: {output_dir}.")
    
    return output_dir
