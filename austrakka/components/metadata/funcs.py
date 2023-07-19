from typing import List

from io import BufferedReader

from austrakka.utils.misc import logger_wraps
from austrakka.utils.api import api_post_multipart
from austrakka.utils.paths import SUBMISSION_PATH
from austrakka.utils.paths import METADATA_SEARCH_PATH
from austrakka.utils.helpers.groups import get_group_by_name
from austrakka.utils.helpers.output import call_get_and_print_table

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
):
    path = "/".join([SUBMISSION_PATH, SUBMISSION_UPLOAD])
    if blanks_will_delete:
        path = f"{path}?{DELETE_ON_BLANK_PARAM}"
    _call_submission(path, file, proforma_abbrev)


@logger_wraps()
def append_metadata(
    file: BufferedReader,
    proforma_abbrev: str,
        blanks_will_delete: bool,
):
    path = "/".join([SUBMISSION_PATH, SUBMISSION_UPLOAD_APPEND])
    if blanks_will_delete:
        path = f"{path}&{DELETE_ON_BLANK_PARAM}"
    _call_submission(path, file, proforma_abbrev)


@logger_wraps()
def validate_metadata(
    file: BufferedReader,
    proforma_abbrev: str,
    is_append: bool
):
    path = SUBMISSION_VALIDATE_APPEND if is_append else SUBMISSION_VALIDATE
    path = "/".join([SUBMISSION_PATH, path])
    _call_submission(path, file, proforma_abbrev)


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
    call_get_and_print_table(
        f'{METADATA_SEARCH_PATH}',
        out_format,
        params={
            'groupContext': group_id
        }
    )

@logger_wraps()
def list_metadata_by_field(group_name: str, field_names: List[str], out_format: str):
    group_id: str = get_group_by_name(group_name)['groupId']
    call_get_and_print_table(
        f'{METADATA_SEARCH_PATH}/{METADATA_BY_FIELD_PATH}',
        out_format,
        params={
            'groupContext': group_id,
            'fields': field_names
        }
    )
