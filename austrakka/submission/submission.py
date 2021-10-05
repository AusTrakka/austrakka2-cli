from io import BufferedReader

from ..utils import logger_wraps
from ..api import call_api
from ..api import post

SUBMISSION_PATH = 'SubmissionSamples'
SUBMISSION_UPLOAD = 'UploadSubmissionSamples'


@logger_wraps()
def add_submission(file: BufferedReader, species_id: int):
    call_api(
        method=post,
        path=f'{SUBMISSION_PATH}/{SUBMISSION_UPLOAD}',
        body={
            'file': (file.name, file),
            'species': str(species_id),
        },
        multipart=True,
    )
