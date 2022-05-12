from os import path
from io import BufferedReader

from austrakka.utils.misc import logger_wraps
from austrakka.utils.api import call_api
from austrakka.utils.api import post
from austrakka.utils.paths import SUBMISSION_PATH

SUBMISSION_UPLOAD = 'UploadSubmissions'


@logger_wraps()
def add_metadata(file: BufferedReader, species_abbrev: str):
    call_api(
        method=post,
        path=path.join(SUBMISSION_PATH, SUBMISSION_UPLOAD),
        body={
            'file': (file.name, file),
            'species-abbrev': species_abbrev,
        },
        multipart=True,
    )
