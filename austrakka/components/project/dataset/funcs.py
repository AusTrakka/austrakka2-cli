import os

from austrakka.utils.fs import get_hash
from austrakka.utils.helpers.upload import upload_multipart
from austrakka.utils.misc import logger_wraps
from austrakka.utils.paths import PROJECT_PATH

DATASET_UPLOAD_PATH = 'dataset'


@logger_wraps()
def add_dataset(
        filepath: str,
        label: str,
        abbrev: str):

    path = "/".join([PROJECT_PATH, abbrev, DATASET_UPLOAD_PATH])
    filename = os.path.basename(filepath)

    custom_headers = {
        'analysis-label': label,
        'filename': filename,
    }

    file_hash = get_hash(filepath)
    with open(filepath, 'rb') as file_content:
        files = [('files[]', (filename, file_content))]
        upload_multipart(path=path,
                         files=files,
                         file_hash=file_hash,
                         custom_headers=custom_headers)
