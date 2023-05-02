from austrakka.utils.api import api_get
from austrakka.utils.paths import PROJECT_PATH


def get_project_by_abbrev(abbrev: str):
    return api_get(path=f"{PROJECT_PATH}/abbrev/{abbrev}")['data']
