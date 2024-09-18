from typing import List

from austrakka.utils.api import api_get
from austrakka.utils.api import api_post
from austrakka.utils.api import api_put
from austrakka.utils.helpers.tenant import get_default_tenant_global_id
from austrakka.utils.misc import logger_wraps
from austrakka.utils.output import print_dict
from austrakka.utils.paths import METADATACOLUMNTYPE_PATH, TENANT_PATH
from austrakka.utils.helpers.fieldtype import get_fieldtype_by_name_v2


@logger_wraps()
def list_fieldtypes(out_format: str):
    tenant_global_id = get_default_tenant_global_id()
    response = api_get(
        path=f"{TENANT_PATH}/{tenant_global_id}/{METADATACOLUMNTYPE_PATH}",
    )

    data = response['data'] if ('data' in response) else response
    for row in data:
        if 'validValues' in row:
            row['validValues'] = ",".join([val['name'] for val in row['validValues']])
    print_dict(data, out_format)


@logger_wraps()
def add_fieldtype(
        name: str,
        description: str,
        valid_values: List[str],
):
    """
    Add a categorical fieldtype (MetaDataColumnType) and its valid values to AusTrakka.
    """
    tenant_global_id = get_default_tenant_global_id()
    api_post(
        path=f"{TENANT_PATH}/{tenant_global_id}/{METADATACOLUMNTYPE_PATH}",
        data={
            "Name": name,
            "Description": description,
            "ValidValues": valid_values,
            "IsActive": True
        }
    )


@logger_wraps()
def update_fieldtype(
        name: str,
        description: str,
        is_active: bool,
):
    tenant_global_id = get_default_tenant_global_id()
    field_type = get_fieldtype_by_name_v2(tenant_global_id, name)

    if description is not None:
        field_type['description'] = description

    if is_active is not None:
        field_type['isActive'] = is_active

    field_type['validValues'] = None

    api_put(
        path=f'{TENANT_PATH}/{tenant_global_id}/{METADATACOLUMNTYPE_PATH}/{field_type["globalId"]}',
        data=field_type
    )
