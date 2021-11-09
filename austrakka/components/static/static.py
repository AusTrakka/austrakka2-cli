from io import BufferedReader

from austrakka.utils.misc import logger_wraps
from austrakka.utils.helpers.upload import upload_file

STATIC_ROUTE = 'StaticTable'
STATIC_UPLOAD = 'Upload'


@logger_wraps()
def add_static(file: BufferedReader, analysis_id: int, species_id: int):
    upload_file(
        file,
        analysis_id,
        species_id,
        f'{STATIC_ROUTE}/{STATIC_UPLOAD}'
    )
