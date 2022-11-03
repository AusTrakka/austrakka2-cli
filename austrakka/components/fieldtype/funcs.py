from typing import List

import pandas as pd

from austrakka.utils.api import call_api
from austrakka.utils.api import get, post, put
from austrakka.utils.misc import logger_wraps
from austrakka.utils.output import print_table
from austrakka.utils.paths import METADATACOLUMNTYPE_PATH
from austrakka.utils.helpers.fieldtype import get_fieldtype_by_name


@logger_wraps()
def list_fieldtypes(out_format: str):
    response = call_api(
        method=get,
        path=METADATACOLUMNTYPE_PATH,
    )

    data = response['data'] if ('data' in response) else response
    for row in data:
        if 'validValues' in row:
            row['validValues'] = [val['name'] for val in row['validValues']]
    result = pd.DataFrame.from_dict(data)

    print_table(
        result,
        out_format,
    )


@logger_wraps()
def add_fieldtype(
        name: str,
        description: str,
        valid_values: List[str],
):
    """
    Add a categorical fieldtype (MetaDataColumnType) and its valid values to AusTrakka.
    """
    call_api(
        method=post,
        path=METADATACOLUMNTYPE_PATH,
        body={
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

    call_api(
        method=put,
        path=f'{METADATACOLUMNTYPE_PATH}/{fieldtype["metaDataColumnTypeId"]}',
        body=fieldtype
    )
