from austrakka.utils.api import api_get
from austrakka.utils.paths import METADATACOLUMN_PATH
from austrakka.utils.helpers import _get_by_identifier


def get_field_by_name(name: str):
    return _get_by_identifier(f'{METADATACOLUMN_PATH}/name', name)


def get_system_field_names():
    response = api_get(
        path=f"{METADATACOLUMN_PATH}/SystemFields?lenient=True",
    )
    data = response['data'] if ('data' in response) else response
    fieldnames = [col['columnName'] for col in data]
    return fieldnames
