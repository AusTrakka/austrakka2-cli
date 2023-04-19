from austrakka.utils.api import api_get
from austrakka.utils.paths import GROUP_PATH


def get_group_by_name(abbrev: str):
    return api_get(path=f"{GROUP_PATH}/{abbrev}")['data']
