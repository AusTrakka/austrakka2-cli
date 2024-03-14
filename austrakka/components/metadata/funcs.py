from typing import List

from pathlib import Path
from io import BufferedReader, StringIO
import codecs

from loguru import logger
import pandas as pd

from austrakka.utils.misc import logger_wraps
from austrakka.utils.api import api_post_multipart
from austrakka.utils.paths import SUBMISSION_PATH
from austrakka.utils.paths import METADATA_SEARCH_PATH
from austrakka.utils.helpers.groups import get_group_by_name
from austrakka.utils.helpers.output import call_get_and_print

SUBMISSION_UPLOAD = 'UploadSubmissions'
SUBMISSION_UPLOAD_APPEND = 'UploadSubmissions?appendMode=True'
SUBMISSION_VALIDATE = 'ValidateSubmissions'
SUBMISSION_VALIDATE_APPEND = 'ValidateSubmissions?appendMode=True'
DELETE_ON_BLANK_PARAM = 'deleteOnBlank=True'

METADATA_BY_FIELD_PATH = 'by-field'

@logger_wraps()
def add_metadata(
        file: BufferedReader,
        proforma_abbrev: str,
        blanks_will_delete: bool,
        batch_size: int,
):
    path = "/".join([SUBMISSION_PATH, SUBMISSION_UPLOAD])
    if blanks_will_delete:
        path = f"{path}?{DELETE_ON_BLANK_PARAM}"
    _call_batched_submission(path, file, proforma_abbrev, batch_size)


@logger_wraps()
def append_metadata(
        file: BufferedReader,
        proforma_abbrev: str,
        blanks_will_delete: bool,
        batch_size: int,
):
    path = "/".join([SUBMISSION_PATH, SUBMISSION_UPLOAD_APPEND])
    if blanks_will_delete:
        path = f"{path}&{DELETE_ON_BLANK_PARAM}"
    _call_batched_submission(path, file, proforma_abbrev, batch_size)


@logger_wraps()
def validate_metadata(
        file: BufferedReader,
        proforma_abbrev: str,
        is_append: bool,
        batch_size: int,
):
    path = SUBMISSION_VALIDATE_APPEND if is_append else SUBMISSION_VALIDATE
    path = "/".join([SUBMISSION_PATH, path])
    _call_batched_submission(path, file, proforma_abbrev, batch_size)

def _call_batched_submission(
        path: str,
        file: BufferedReader,
        proforma_abbrev: str,
        batch_size: int
):
    if batch_size < 1:
        _call_submission(path, file, proforma_abbrev)
        return
    
    filepath = Path(file.name)
    if  filepath.suffix == '.csv':
        # pylint: disable=C0103
        df = pd.read_csv(file, dtype=str, index_col=False, keep_default_na=False, na_values='')
    elif filepath.suffix == '.xlsx':
        # Batching not currently supported, just upload the original file
        _call_submission(path, file, proforma_abbrev)
        return
    else:
        raise ValueError('File must be .csv or .xlsx')
    
    num_rows = df.shape[0]
    if num_rows <= batch_size:
        # Just upload the original file
        file.seek(0)
        _call_submission(path, file, proforma_abbrev)
        return
    
    logger.info(f"Uploading {num_rows} rows in batches of {batch_size}")
    encode = codecs.getwriter('utf-8')
    for index in range(0, num_rows, batch_size):
        logger.info(f"Uploading rows {index}-{index+batch_size-1}")
        chunk = df.iloc[index:index+batch_size, :]
        buffer = StringIO()
        buffer.name = f"{filepath.stem}_batch_rows{index}-{index+batch_size-1}.csv"
        chunk.to_csv(buffer, index=False)
        _call_submission(path, encode(buffer), proforma_abbrev)
    
    logger.info("Batched upload complete")


def _call_submission(
        path: str,
        file: BufferedReader,
        proforma_abbrev: str,
):
    api_post_multipart(
        path=path,
        data={
            'proforma-abbrev': proforma_abbrev,
        },
        files={'file': (file.name, file)}
    )


@logger_wraps()
def list_metadata(group_name: str, out_format: str):
    group_id: str = get_group_by_name(group_name)['groupId']
    call_get_and_print(
        f'{METADATA_SEARCH_PATH}',
        out_format,
        params={
            'groupContext': group_id
        }
    )

@logger_wraps()
def list_metadata_by_field(group_name: str, field_names: List[str], out_format: str):
    group_id: str = get_group_by_name(group_name)['groupId']
    call_get_and_print(
        f'{METADATA_SEARCH_PATH}/{METADATA_BY_FIELD_PATH}',
        out_format,
        params={
            'groupContext': group_id,
            'fields': field_names
        }
    )
