from typing import List

from austrakka.utils.api import call_api
from austrakka.utils.api import post
from austrakka.utils.misc import logger_wraps
from austrakka.utils.paths import METADATACOLUMNTYPE_PATH


@logger_wraps()
def add_fieldtype_values(name: str, field_values: List[str]):
    return call_api(
        method=post,
        path=f'{METADATACOLUMNTYPE_PATH}/addValues/{name}',
        body=field_values
    )


@logger_wraps()
def remove_fieldtype_values(name: str, field_values: List[str]):
    return call_api(
        method=post,
        path=f'{METADATACOLUMNTYPE_PATH}/removeValues/{name}',
        body=field_values
    )
