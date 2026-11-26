from typing import List

from trakka.utils.api import api_get
from trakka.utils.api import api_post
from trakka.utils.api import api_put
from trakka.utils.misc import logger_wraps
from trakka.utils.output import print_dict
from trakka.utils.paths import METADATA_COLUMN_TYPE_V2_PATH
from trakka.utils.helpers.fieldtype import get_fieldtype_by_name_v2


@logger_wraps()
def list_fieldtypes(out_format: str):
    response = api_get(
        path=f"{METADATA_COLUMN_TYPE_V2_PATH}",
    )

    data = response['data'] if ('data' in response) else response
    for row in data:
        if 'validValues' in row:
            row['validValues'] = ";".join([val['name'] for val in row['validValues']])
    print_dict(data, out_format)


@logger_wraps()
def add_fieldtype(
        name: str,
        description: str,
        valid_values: List[str],
        is_multi_valued: bool,
):
    """
    Add a categorical fieldtype and its valid values
    """
    api_post(
        path=f"{METADATA_COLUMN_TYPE_V2_PATH}",
        data={
            "Name": name,
            "Description": description,
            "ValidValues": valid_values,
            "IsActive": True,
            "IsMultiValued": is_multi_valued,
        }
    )


@logger_wraps()
def update_fieldtype(
        name: str,
        description: str,
        is_active: bool,
        is_multi_valued: bool,
):
    field_type = get_fieldtype_by_name_v2(name)

    if description is not None:
        field_type['description'] = description

    if is_active is not None:
        field_type['isActive'] = is_active

    if is_multi_valued is not None:
        field_type['isMultiValued'] = is_multi_valued

    field_type['validValues'] = None

    api_put(
        path=f'{METADATA_COLUMN_TYPE_V2_PATH}/{name}',
        data=field_type
    )
