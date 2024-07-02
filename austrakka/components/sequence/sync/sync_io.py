# pylint: disable=broad-exception-caught
import os
import json
import hashlib
import pandas as pd

from .constant import INTERMEDIATE_MANIFEST_FILE_KEY
from .constant import OUTPUT_DIR_KEY
from .errors import SyncError

invalid_output_dir = [
    '/', '/usr', '/home', '/bin', '/sbin', '/var', '/etc', '/opt'
]


def save_json(dict_obj: dict, path: str):
    with open(path, 'w', encoding='UTF-8') as file:
        json.dump(dict_obj, file)


def read_sync_state(path: str) -> dict:
    if os.path.exists(path):
        with open(path, encoding='UTF-8') as file:
            return json.load(file)
    else:
        return {}


def read_from_csv(sync_state: dict, state_key: str):
    path = get_path(sync_state, state_key)
    data_frame = pd.read_csv(path)
    return data_frame


def read_from_csv_or_empty(sync_state: dict, state_key: str) -> pd.DataFrame:
    path = get_path(sync_state, state_key)
    try:
        data_frame = pd.read_csv(path, dtype=str, index_col=False)
        return data_frame
    except Exception:
        return pd.DataFrame()


def save_int_manifest(data_frame, sync_state):
    path = get_path(sync_state, INTERMEDIATE_MANIFEST_FILE_KEY)
    with open(path, 'w', encoding='UTF-8') as file:
        data_frame.to_csv(file, index=False)
        file.close()


def save_to_csv(data_frame, path):
    with open(path, 'w', encoding='UTF-8') as file:
        data_frame.to_csv(file, index=False)
        file.close()


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


def calc_hash(path):
    with open(path, 'rb') as file:
        file_hash = hashlib.sha256(file.read()).hexdigest().lower()
        file.close()
    return file_hash
