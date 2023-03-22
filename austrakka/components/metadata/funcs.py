from io import BufferedReader

from austrakka.utils.misc import logger_wraps
from austrakka.utils.api import api_post_multipart
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
    path = "/".join([SUBMISSION_PATH, SUBMISSION_UPLOAD])
    _call_submission(path, file, proforma_abbrev)


@logger_wraps()
def append_metadata(
    file: BufferedReader,
    proforma_abbrev: str
):
    path = "/".join([SUBMISSION_PATH, SUBMISSION_UPLOAD_APPEND])
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
