from typing import List

from trakka.utils.api import api_post
from trakka.utils.misc import logger_wraps
from trakka.utils.paths import METADATA_COLUMN_TYPE_V2_PATH


@logger_wraps()
def add_fieldtype_values(name: str, field_values: List[str]):
    return api_post(
        path=f'{METADATA_COLUMN_TYPE_V2_PATH}/addValues/{name}',
        data=field_values
    )


@logger_wraps()
def remove_fieldtype_values(name: str, field_values: List[str]):
    return api_post(
        path=f'{METADATA_COLUMN_TYPE_V2_PATH}/removeValues/{name}',
        data=field_values
    )
