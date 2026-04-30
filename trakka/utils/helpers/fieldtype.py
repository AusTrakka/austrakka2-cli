from trakka.utils.api import api_get
from trakka.utils.paths import METADATA_COLUMN_TYPE_V2_PATH


def get_fieldtype_by_name_v2(name: str):
    return api_get(
        path=f"{METADATA_COLUMN_TYPE_V2_PATH}/name/{name}")['data']
