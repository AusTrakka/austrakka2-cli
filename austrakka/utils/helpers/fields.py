from austrakka.utils.api import api_get
from austrakka.utils.paths import METADATACOLUMNS_PATH
from austrakka.utils.paths import METADATA_COLUMN_V2_PATH

def get_field_by_name(name: str):
    return api_get(path=f"{METADATACOLUMNS_PATH}/name/{name}")['data']

def get_field_by_name_v2(name: str):
    return api_get(
        path=f"{METADATA_COLUMN_V2_PATH}/name/{name}")['data']
