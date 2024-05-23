from typing import List

import pandas as pd

from austrakka.utils.api import api_get
from austrakka.utils.api import api_patch
from austrakka.utils.misc import logger_wraps
from austrakka.utils.output import print_dataframe
from austrakka.utils.paths import GROUP_PATH


@logger_wraps()
def add_field_group(name: str, field_names: List[str]):

    field_name_objs = []
    for field_name in field_names:
        field_name_objs.append({
            "ColumnName": field_name
        })

    return api_patch(
        path=f'{GROUP_PATH}/allow-fields/{name}',
        data={
            "columnNames": field_name_objs
        }
    )


@logger_wraps()
def remove_field_group(name: str, field_names: List[str]):

    field_name_objs = []
    for field_name in field_names:
        field_name_objs.append({
            "ColumnName": field_name
        })

    return api_patch(
        path=f'{GROUP_PATH}/deny-fields/{name}',
        data={
            "columnNames": field_name_objs
        }
    )


@logger_wraps()
def list_field_group(name: str, out_format: str):

    response = api_get(
        path=f'{GROUP_PATH}/allowed-fields/{name}',
    )

    data = response['data'] if ('data' in response) else response
    result = pd.json_normalize(data, max_level=1)

    print_dataframe(
        result,
        out_format,
    )
