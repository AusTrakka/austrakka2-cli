from typing import List

from austrakka.utils.api import api_post
from austrakka.utils.misc import logger_wraps
from austrakka.utils.paths import METADATACOLUMNTYPE_PATH


@logger_wraps()
def add_fieldtype_values(name: str, field_values: List[str]):
    return api_post(
        path=f'{METADATACOLUMNTYPE_PATH}/addValues/{name}',
        data=field_values
    )


@logger_wraps()
def remove_fieldtype_values(name: str, field_values: List[str]):
    return api_post(
        path=f'{METADATACOLUMNTYPE_PATH}/removeValues/{name}',
        data=field_values
    )
