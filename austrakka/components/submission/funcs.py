from io import BufferedReader

from austrakka.utils.misc import logger_wraps
from austrakka.utils.api import call_api
from austrakka.utils.api import post

SUBMISSION_PATH = 'SubmissionSamples'
SUBMISSION_UPLOAD = 'UploadSubmissionSamples'


@logger_wraps()
def add_submission(file: BufferedReader, species_id: int):
    call_api(
        method=post,
        path=f'{SUBMISSION_PATH}/{SUBMISSION_UPLOAD}',
        body={
            'file': (file.name, file),
            'speciesid': str(species_id),
        },
        multipart=True,
    )
