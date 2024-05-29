from typing import List
from loguru import logger

from austrakka.utils.api import api_patch, api_get
from austrakka.utils.misc import logger_wraps
from austrakka.utils.output import print_dict
from austrakka.utils.paths import PROJECT_PATH


@logger_wraps()
def add_provision_project(abbrev: str, field_names: List[str]):
    field_name_objs = convert_to_api_dto(field_names)

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
    field_name_objs = convert_to_api_dto(field_names)

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

    print_dict(
        data,
        out_format,
    )


def convert_to_api_dto(field_names):
    field_name_objs = []
    for field_name in field_names:
        field_name_objs.append({
            "ColumnName": field_name
        })
    return field_name_objs
