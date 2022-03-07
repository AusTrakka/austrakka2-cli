from os import path
from io import BufferedReader

from austrakka.utils.misc import logger_wraps
from austrakka.utils.helpers.upload import upload_file
from austrakka.utils.paths import TREE_PATH

TREE_UPLOAD = 'UploadTree'


@logger_wraps()
def add_tree(file: BufferedReader, analysis_id: int, species_id: int):
    upload_file(
        file,
        analysis_id,
        species_id,
        path.join(TREE_PATH, TREE_UPLOAD)
    )
