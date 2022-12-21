from io import BufferedReader

from austrakka.utils.misc import logger_wraps
from austrakka.utils.api import call_api
from austrakka.utils.api import post
from austrakka.utils.paths import SUBMISSION_PATH

SUBMISSION_UPLOAD = 'UploadSubmissions'
SUBMISSION_UPLOAD_APPEND = 'UploadSubmissions?appendMode=True'
SUBMISSION_VALIDATE = 'ValidateSubmissions'
SUBMISSION_VALIDATE_APPEND = 'ValidateSubmissions?appendMode=True'


@logger_wraps()
def add_metadata(
    file: BufferedReader,
    proforma_abbrev: str
):
    call_api(
        method=post,
        path="/".join([SUBMISSION_PATH, SUBMISSION_UPLOAD]),
        body={
            'file': (file.name, file),
            'proforma-abbrev': proforma_abbrev,
        },
        multipart=True,
    )


@logger_wraps()
def append_metadata(
    file: BufferedReader,
    proforma_abbrev: str
):
    call_api(
        method=post,
        path="/".join([SUBMISSION_PATH, SUBMISSION_UPLOAD_APPEND]),
        body={
            'file': (file.name, file),
            'proforma-abbrev': proforma_abbrev,
        },
        multipart=True,
    )


@logger_wraps()
def validate_metadata(
    file: BufferedReader,
    proforma_abbrev: str,
    is_append: bool
):
    path = SUBMISSION_VALIDATE_APPEND if is_append else SUBMISSION_VALIDATE
    call_api(
        method=post,
        path="/".join([SUBMISSION_PATH, path]),
        body={
            'file': (file.name, file),
            'proforma-abbrev': proforma_abbrev,
        },
        multipart=True,
    )
