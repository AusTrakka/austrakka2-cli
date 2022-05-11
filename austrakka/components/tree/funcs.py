from os import path
from io import BufferedReader

from austrakka.utils.misc import logger_wraps
from austrakka.utils.helpers.upload import upload_file
from austrakka.utils.paths import TREE_PATH

TREE_UPLOAD = 'UploadTree'


@logger_wraps()
def add_tree(file: BufferedReader, analysis_abbrev: str):
    upload_file(
        file,
        analysis_abbrev,
        path.join(TREE_PATH, TREE_UPLOAD)
    )
