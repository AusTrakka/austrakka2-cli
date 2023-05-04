from austrakka.utils.api import api_get
from austrakka.utils.paths import METADATACOLUMN_PATH


def get_field_by_name(name: str):
    return api_get(path=f"{METADATACOLUMN_PATH}/name/{name}")['data']


def get_system_field_names():
    response = api_get(
        path=f"{METADATACOLUMN_PATH}/SystemFields?lenient=True",
    )
    data = response['data'] if ('data' in response) else response
    fieldnames = [col['columnName'] for col in data]
    return fieldnames
