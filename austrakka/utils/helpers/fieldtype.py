from austrakka.utils.api import api_get
from austrakka.utils.paths import METADATACOLUMNTYPE_PATH


def get_fieldtype_by_name(name: str):
    response = api_get(
        path=f"{METADATACOLUMNTYPE_PATH}/name/{name}"
    )
    return response['data'] if ('data' in response) else response
