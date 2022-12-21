
from austrakka.utils.api import call_api
from austrakka.utils.api import get
from ..paths import METADATACOLUMNTYPE_PATH, METADATACOLUMN_PATH


def get_fieldtype_by_name(name: str):
    response = call_api(
        method=get,
        path=f"{METADATACOLUMNTYPE_PATH}/name/{name}",
    )
    return response['data'] if ('data' in response) else response


def get_field_by_name(name: str):
    response = call_api(
        method=get,
        path=f"{METADATACOLUMN_PATH}/name/{name}"
    )
    return response['data'] if ('data' in response) else response


def get_system_field_names():
    response = call_api(
        method=get,
        path=f"{METADATACOLUMN_PATH}/SystemFields?lenient=True",
    )
    data = response['data'] if ('data' in response) else response
    fieldnames = [col['columnName'] for col in data]
    return fieldnames
