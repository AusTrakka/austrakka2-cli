from typing import List
from loguru import logger
import pandas as pd
from austrakka.utils.api import api_patch, api_get
from austrakka.utils.misc import logger_wraps
from austrakka.utils.output import print_table
from austrakka.utils.paths import PROJECT_PATH

# pylint: disable=duplicate-code
@logger_wraps()
def add_field_project(abbrev: str, field_names: List[str]):
    field_name_objs = {"fieldAndSourceDTOs": []}
    for field_name in field_names:
        field_name_split = field_name.split(',')
        field_name_objs["fieldAndSourceDTOs"].append({
            "fieldName": field_name_split[0],
            "restrictionName": field_name_split[1].replace('-', ' ')
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
        path=f'{PROJECT_PATH}/{abbrev}/add-project-view-provision',
        data={
            "columnNames": field_name_objs
        }
    )


@logger_wraps()
def remove_project_provision(abbrev: str, provision_id: str):
    return api_patch(
        path=f'{PROJECT_PATH}/{abbrev}/remove-project-view-provision/{provision_id}'
    )


@logger_wraps()
def update_project_provision(abbrev: str, provision_id: str, field_names: List[str]):
    field_name_objs = []
    for field_name in field_names:
        field_name_objs.append({
            "ColumnName": field_name
        })

    return api_patch(
        path=f'{PROJECT_PATH}/{abbrev}/update-project-view-provision/{provision_id}',
        data={
            "columnNames": field_name_objs
        }
    )

@logger_wraps()
def get_dataset_provision_list(
        abbrev: str,
        out_format: str):
    path = "/".join([PROJECT_PATH, abbrev, 'project-provision-list'])
    response = api_get(path)
    data = response['data'] if ('data' in response) else response
    if not data:
        logger.info("No Dataset Provisions available")
        return

    result = pd.DataFrame.from_dict(data)
    print_table(
        result,
        out_format,
    )


@logger_wraps()
def get_project_field_list(
        abbrev: str,
        out_format: str):
    path = "/".join([PROJECT_PATH, abbrev, 'project-field-list'])
    response = api_get(path)
    data = response['data'] if ('data' in response) else response
    if not data:
        logger.info("No Project Fields available")
        return

    result = pd.DataFrame.from_dict(data)
    print_table(
        result,
        out_format,
    )


@logger_wraps()
def remove_project_field(abbrev: str, field_names: List[str]):

    return api_patch(
        path=f'{PROJECT_PATH}/remove-project-field/{abbrev}',
        data=field_names
    )
