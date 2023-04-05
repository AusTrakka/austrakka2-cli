from austrakka.utils.api import api_get
from ..paths import ORG_PATH


def get_org_by_abbrev(abbrev: str):
    response = api_get(
        path=f"{ORG_PATH}/{abbrev}"
    )
    return response['data'] if ('data' in response) else response
