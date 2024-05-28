from typing import List

from austrakka.utils.api import api_get
from austrakka.utils.api import api_post
from austrakka.utils.api import api_put
from austrakka.utils.misc import logger_wraps
from austrakka.utils.output import print_dict
from austrakka.utils.paths import METADATACOLUMNTYPE_PATH
from austrakka.utils.helpers.fieldtype import get_fieldtype_by_name


@logger_wraps()
def list_fieldtypes(out_format: str):
    response = api_get(
        path=METADATACOLUMNTYPE_PATH,
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
        path=METADATACOLUMNTYPE_PATH,
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
    fieldtype = get_fieldtype_by_name(name)

    if description is not None:
        fieldtype['description'] = description

    if is_active is not None:
        fieldtype['isActive'] = is_active

    fieldtype['validValues'] = None

    api_put(
        path=f'{METADATACOLUMNTYPE_PATH}/{fieldtype["metaDataColumnTypeId"]}',
        data=fieldtype
    )
