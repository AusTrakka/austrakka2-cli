from os import path
from io import BufferedReader

from austrakka.utils.api import api_patch
from austrakka.utils.helpers.output import call_get_and_print
from austrakka.utils.misc import logger_wraps
from austrakka.utils.helpers.upload import upload_file
from austrakka.utils.paths import TREE_PATH
from austrakka.utils.paths import JOB_INSTANCE_PATH
from austrakka.utils.helpers.analysis import get_analysis_by_abbrev

TREE_UPLOAD = 'UploadTree'
ALL_VERSIONS = 'AllVersions'


@logger_wraps()
def add_tree(file: BufferedReader, analysis_abbrev: str):
    upload_file(
        file,
        analysis_abbrev,
        path.join(TREE_PATH, TREE_UPLOAD)
    )


@logger_wraps()
def list_trees(out_format: str, analysis_abbrev: str):
    analysis = get_analysis_by_abbrev(analysis_abbrev)
    call_get_and_print(
        f'{JOB_INSTANCE_PATH}/{analysis["analysisId"]}/{ALL_VERSIONS}',
        out_format
    )


@logger_wraps()
def disable_tree(tree_id: int):
    api_patch(path=f'{TREE_PATH}/disable/{tree_id}')


@logger_wraps()
def enable_tree(tree_id: int):
    api_patch(path=f'{TREE_PATH}/enable/{tree_id}')
