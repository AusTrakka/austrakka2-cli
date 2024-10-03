from austrakka.utils.api import api_get
from austrakka.utils.paths import METADATACOLUMNTYPE_PATH, TENANT_PATH


def get_fieldtype_by_name(name: str):
    return api_get(path=f"{METADATACOLUMNTYPE_PATH}/name/{name}")['data']


def get_fieldtype_by_name_v2(tenant_global_id: str, name: str):
    return api_get(
        path=f"{TENANT_PATH}/{tenant_global_id}/{METADATACOLUMNTYPE_PATH}/name/{name}")['data']
