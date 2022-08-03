from austrakka.utils.api import call_api
from austrakka.utils.api import get
from ..paths import ORG_PATH


def get_org_by_abbrev(abbrev: str):
    response = call_api(
        method=get,
        path=f"{ORG_PATH}/abbrev/{abbrev}"
    )
    return response['data'] if ('data' in response) else response
