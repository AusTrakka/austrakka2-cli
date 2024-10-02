from typing import List

from austrakka.utils.api import api_post
from austrakka.utils.helpers.tenant import get_default_tenant_global_id
from austrakka.utils.misc import logger_wraps
from austrakka.utils.paths import METADATACOLUMNTYPE_PATH, TENANT_PATH


@logger_wraps()
def add_fieldtype_values(name: str, field_values: List[str]):
    tenant_global_id = get_default_tenant_global_id()
    return api_post(
        path=f'{TENANT_PATH}/{tenant_global_id}/{METADATACOLUMNTYPE_PATH}/addValues/{name}',
        data=field_values
    )


@logger_wraps()
def remove_fieldtype_values(name: str, field_values: List[str]):
    tenant_global_id = get_default_tenant_global_id()
    return api_post(
        path=f'{TENANT_PATH}/{tenant_global_id}/{METADATACOLUMNTYPE_PATH}/removeValues/{name}',
        data=field_values
    )
