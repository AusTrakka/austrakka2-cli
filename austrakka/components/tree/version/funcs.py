from os import path
from io import BufferedReader

from austrakka.utils.api import api_patch, api_post_multipart
from austrakka.utils.helpers.output import call_get_and_print
from austrakka.utils.misc import logger_wraps
from austrakka.utils.paths import TREE_VERSION_PATH
from austrakka.utils.helpers.tree import get_tree_by_abbrev

TREE_UPLOAD = 'UploadTree'
ALL_VERSIONS = 'AllVersions'


@logger_wraps()
def add_tree_version(file: BufferedReader, tree_abbrev: str):
    tree = get_tree_by_abbrev(tree_abbrev)
    api_post_multipart(
        path=path.join(TREE_VERSION_PATH, TREE_UPLOAD),
        data={
            'treeid': str(tree['treeId'])
        },
        files={'file': (file.name, file)}
    )


@logger_wraps()
def list_tree_versions(out_format: str, tree_abbrev: str):
    tree = get_tree_by_abbrev(tree_abbrev)
    call_get_and_print(
        f'{TREE_VERSION_PATH}/{tree["treeId"]}/{ALL_VERSIONS}',
        out_format
    )


@logger_wraps()
def disable_tree_version(tree_id: int):
    api_patch(path=f'{TREE_VERSION_PATH}/disable/{tree_id}')


@logger_wraps()
def enable_tree_version(tree_id: int):
    api_patch(path=f'{TREE_VERSION_PATH}/enable/{tree_id}')
