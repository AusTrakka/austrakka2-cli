from os import path
from io import BufferedReader

from austrakka.utils.misc import logger_wraps
from austrakka.utils.helpers.upload import upload_file
from austrakka.utils.paths import STATIC_PATH

STATIC_UPLOAD = 'Upload'


@logger_wraps()
def add_static(file: BufferedReader, analysis_id: int):
    upload_file(
        file,
        analysis_id,
        path.join(STATIC_PATH, STATIC_UPLOAD)
    )
