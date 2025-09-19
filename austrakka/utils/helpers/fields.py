from austrakka.utils.api import api_get
from austrakka.utils.paths import METADATACOLUMNS_PATH, TENANT_PATH, METADATACOLUMN_PATH

def get_field_by_name(name: str):
    return api_get(path=f"{METADATACOLUMNS_PATH}/name/{name}")['data']


def get_field_by_name_v2(tenant_global_id:str, name: str):
    return api_get(
        path=f"{TENANT_PATH}/{tenant_global_id}/{METADATACOLUMN_PATH}/name/{name}")['data']

