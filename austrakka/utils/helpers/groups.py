from austrakka.utils.api import api_get
from austrakka.utils.paths import GROUP_PATH


def get_group_by_name(name: str):
    return api_get(path=f"{GROUP_PATH}/{name}")['data']
