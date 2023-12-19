from typing import List

from austrakka.utils.api import api_patch
from austrakka.utils.misc import logger_wraps
from austrakka.utils.paths import PROJECT_PATH

# pylint: disable=duplicate-code
@logger_wraps()
def add_field_project(abbrev: str, field_names: List[str]):
    field_name_objs = {"fieldAndSourceDTOs": []}
    for field_name in field_names:
        field_name_split = field_name.split(',')
        field_name_objs["fieldAndSourceDTOs"].append({
            "fieldName": field_name_split[0],
            "restrictionName": field_name_split[1]
        })

    # Replace 'abbrev' with your actual value
    return api_patch(
        path=f'{PROJECT_PATH}/add-project-field/{abbrev}',
        data=field_name_objs
    )


@logger_wraps()
def set_merge_algorithm_project(abbrev: str, merge_algorithm: str):
    if merge_algorithm == 'show-all':
        merge_algorithm = 'ShowAll'
    else:
        merge_algorithm = 'Override'

    return api_patch(
        path=f'{PROJECT_PATH}/{abbrev}/set-merge-algorithm/{merge_algorithm}'
    )


@logger_wraps()
def add_provision_project(abbrev: str, field_names: List[str]):
    field_name_objs = []
    for field_name in field_names:
        field_name_objs.append({
            "ColumnName": field_name
        })

    return api_patch(
        path=f'{PROJECT_PATH}/{abbrev}/set-project-view-provision',
        data={
            "columnNames": field_name_objs
        }
    )
