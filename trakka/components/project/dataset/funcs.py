# pylint: disable=R0801
import os
import time

from loguru import logger
from trakka.utils.api import api_get, api_patch
from trakka.utils.fs import get_hash
from trakka.utils.helpers.output import call_get_and_print
from trakka.utils.helpers.upload import upload_multipart
from trakka.utils.misc import logger_wraps
from trakka.utils.output import print_dict
from trakka.utils.paths import PROJECT_PATH

DATASET_UPLOAD_PATH = 'dataset'
DATASET_ACK_PATH = 'acknowledge'
DATASET_TRACK_PATH = 'dataset-progress'
DATASET_TRACK_DETAILED_PATH = 'dataset-progress-details'


@logger_wraps()
def add_dataset(
        filepath: str,
        label: str,
        abbrev: str
):
    path_adding = "/".join([PROJECT_PATH, abbrev, DATASET_UPLOAD_PATH])
    filename = os.path.basename(filepath)

    custom_headers = {
        'analysis-label': label,
    }

    file_hash = get_hash(filepath)
    with open(filepath, 'rb') as file_content:
        files = [('files[]', (filename, file_content))]
        upload_multipart(path=path_adding,
                         files=files,
                         file_hash=file_hash,
                         custom_headers=custom_headers)


@logger_wraps()
def disable_dataset(
        abbrev: str,
        dataset_id: int):
    path = "/".join([PROJECT_PATH, abbrev, 'disable-dataset', str(dataset_id)])
    return api_patch(
        path=path,
    )


@logger_wraps()
def list_dataset(abbrev: str, out_format: str):
    path = "/".join([PROJECT_PATH, abbrev, 'active-dataset-entry-list'])
    call_get_and_print(path, out_format)
