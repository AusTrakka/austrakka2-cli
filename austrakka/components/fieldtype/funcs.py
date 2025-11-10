from typing import List

from austrakka.utils.api import api_get
from austrakka.utils.api import api_post
from austrakka.utils.api import api_put
from austrakka.utils.misc import logger_wraps
from austrakka.utils.output import print_dict
from austrakka.utils.paths import METADATA_COLUMN_TYPE_V2_PATH
from austrakka.utils.helpers.fieldtype import get_fieldtype_by_name_v2


@logger_wraps()
def list_fieldtypes(out_format: str):
    response = api_get(
        path=f"{METADATA_COLUMN_TYPE_V2_PATH}",
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
    api_post(
        path=f"{METADATA_COLUMN_TYPE_V2_PATH}",
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
    field_type = get_fieldtype_by_name_v2(name)

    if description is not None:
        field_type['description'] = description

    if is_active is not None:
        field_type['isActive'] = is_active

    field_type['validValues'] = None

    api_put(
        path=f'{METADATA_COLUMN_TYPE_V2_PATH}/{field_type["globalId"]}',
        data=field_type
    )
