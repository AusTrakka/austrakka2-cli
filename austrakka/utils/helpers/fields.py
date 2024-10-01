from austrakka.utils.api import api_get
from austrakka.utils.paths import METADATACOLUMNS_PATH, TENANT_PATH, METADATACOLUMN_PATH


def get_field_by_name(name: str):
    return api_get(path=f"{METADATACOLUMNS_PATH}/name/{name}")['data']


def get_field_by_name_v2(tenant_global_id:str, name: str):
    return api_get(
        path=f"{TENANT_PATH}/{tenant_global_id}/{METADATACOLUMN_PATH}/name/{name}")['data']


def get_system_field_names():
    response = api_get(
        path=f"{METADATACOLUMNS_PATH}/SystemFields?lenient=True",
    )
    data = response['data'] if ('data' in response) else response
    fieldnames = [col['columnName'] for col in data]
    return fieldnames


def get_system_field_names_v2(tenant_global_id: str):
    response = api_get(
        path=f"{TENANT_PATH}/{tenant_global_id}/{METADATACOLUMN_PATH}/SystemFields?lenient=True",
    )
    data = response['data'] if ('data' in response) else response
    fieldnames = [col['columnName'] for col in data]
    return fieldnames
