from io import BufferedReader

from ..utils import logger_wraps
from ..api import call_api
from ..api import post

TREE_PATH = 'Tree'
TREE_UPLOAD = 'UploadTree'


@logger_wraps()
def add_tree(file: BufferedReader, analysis_id: int):
    call_api(
        method=post,
        path=f'{TREE_PATH}/{TREE_UPLOAD}',
        body={
            'file': (file.name, file),
            'analysisid': str(analysis_id),
        },
        multipart=True,
    )
