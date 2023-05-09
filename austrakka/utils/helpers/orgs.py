from austrakka.utils.api import api_get
from austrakka.utils.paths import ORG_PATH


def get_org_by_abbrev(abbrev: str):
    return api_get(path=f"{ORG_PATH}/{abbrev}")['data']
