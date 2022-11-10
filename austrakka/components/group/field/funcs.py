from typing import List

import pandas as pd

from austrakka.utils.api import call_api
from austrakka.utils.api import get, patch
from austrakka.utils.misc import logger_wraps
from austrakka.utils.output import print_table
from austrakka.utils.paths import GROUP_PATH


@logger_wraps()
def add_field_group(name: str, field_names: List[str]):

    field_name_objs = []
    for field_name in field_names:
        field_name_objs.append({
            "ColumnName": field_name
        })

    return call_api(
        method=patch,
        path=f'{GROUP_PATH}/allow-fields/{name}',
        body={
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

    return call_api(
        method=patch,
        path=f'{GROUP_PATH}/deny-fields/{name}',
        body={
            "columnNames": field_name_objs
        }
    )


@logger_wraps()
def list_field_group(name: str, out_format: str):

    response = call_api(
        method=get,
        path=f'{GROUP_PATH}/allowed-fields/{name}',
    )

    data = response['data'] if ('data' in response) else response
    result = pd.json_normalize(data, max_level=1)

    print_table(
        result,
        out_format,
    )
