from typing import List

from trakka.utils.api import api_get
from trakka.utils.api import api_patch
from trakka.utils.misc import logger_wraps
from trakka.utils.output import print_dataframe, read_pd
from trakka.utils.paths import GROUP_PATH


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
    result = read_pd(data, out_format)

    print_dataframe(
        result,
        out_format,
    )
