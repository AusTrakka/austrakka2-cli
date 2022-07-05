from austrakka.utils.api import call_api
from austrakka.utils.api import get
from ..paths import ORG_PATH


def get_org_by_id(identifier: int):
    response = call_api(
        method=get,
        path=f"{ORG_PATH}/{identifier}"
    )
    return response['data'] if ('data' in response) else response
