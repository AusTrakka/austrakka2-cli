from typing import List

from austrakka.utils.api import api_patch
from austrakka.utils.misc import logger_wraps
from austrakka.utils.paths import PROJECT_PATH

# pylint: disable=duplicate-code
@logger_wraps()
def add_field_project(abbrev: str, field_names: List[str]):

    field_name_objs = []
    for field_name in field_names:
        field_name_objs.append({
            "ColumnName": field_name
        })

    return api_patch(
        path=f'{PROJECT_PATH}/add-project-field/{abbrev}',
        data={
            "columnNames": field_name_objs
        }
    )
