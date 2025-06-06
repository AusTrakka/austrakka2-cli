from austrakka.utils.api import api_get
from austrakka.utils.paths import TREE_PATH


def get_tree_by_abbrev(abbrev: str):
    return api_get(path=f"{TREE_PATH}/abbrev/{abbrev}")['data']
