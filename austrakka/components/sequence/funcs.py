from io import BufferedReader
from typing import Tuple
from os import path

from austrakka.utils.misc import logger_wraps
from austrakka.utils.api import call_api
from austrakka.utils.api import post
from austrakka.utils.paths import SEQUENCE_PATH

SEQUENCE_UPLOAD = 'Fasta'


@logger_wraps()
def add_sequence_submission(files: Tuple[BufferedReader], csv: BufferedReader):
    call_api(
        method=post,
        path=path.join(SEQUENCE_PATH, SEQUENCE_UPLOAD),
        body=[('files[]', (file.name, file)) for file in files]
        + [('files[]', (csv.name, csv))],
        multipart=True,
    )
