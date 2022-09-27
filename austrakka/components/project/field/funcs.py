from typing import List

import pandas as pd

from austrakka.utils.api import call_api
from austrakka.utils.api import patch, get
from austrakka.utils.misc import logger_wraps
from austrakka.utils.paths import PROJECT_PATH
from austrakka.utils.output import print_table


@logger_wraps()
def set_field_project(abbrev: str, field_names: List[str]):

    field_name_objs = []
    for field_name in field_names:
        field_name_objs.append({
            "ColumnName": field_name
        })

    return call_api(
        method=patch,
        path=f'{PROJECT_PATH}/set-fields/{abbrev}',
        body={
            "columnNames": field_name_objs
        }
    )


@logger_wraps()
def unset_field_project(abbrev: str, field_names: List[str]):

    field_name_objs = []
    for field_name in field_names:
        field_name_objs.append({
            "ColumnName": field_name
        })

    return call_api(
        method=patch,
        path=f'{PROJECT_PATH}/unset-fields/{abbrev}',
        body={
            "columnNames": field_name_objs
        }
    )


@logger_wraps()
def display_field_project(abbrev: str, table_format):

    response = call_api(
        method=get,
        path=f'{PROJECT_PATH}/display-fields/{abbrev}',
    )

    data = response['data'] if ('data' in response) else response
    result = pd.json_normalize(data, max_level=1)

    print_table(
        result,
        table_format,
    )
