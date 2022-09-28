from austrakka.utils.api import call_api
from austrakka.utils.api import get
from austrakka.utils.paths import METADATACOLUMNTYPE_PATH


def get_fieldtype_by_name(name: str):
    response = call_api(
        method=get,
        path=f"{METADATACOLUMNTYPE_PATH}/name/{name}"
    )
    return response['data'] if ('data' in response) else response
