from io import BufferedReader

from austrakka.utils.misc import logger_wraps
from austrakka.utils.api import call_api
from austrakka.utils.api import post
from ..enums import SUBMISSION_PATH


SUBMISSION_UPLOAD = 'UploadSequenceFile'


@logger_wraps()
def add_sequence_submission(file: BufferedReader):
    call_api(
        method=post,
        path=f'{SUBMISSION_PATH}/{SUBMISSION_UPLOAD}',
        body={
            'files': (file.name, file)
        },
        multipart=True,
    )
