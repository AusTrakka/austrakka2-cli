from typing import List
from loguru import logger
import pandas as pd
from austrakka.utils.api import api_patch, api_get
from austrakka.utils.misc import logger_wraps
from austrakka.utils.output import print_formatted
from austrakka.utils.paths import PROJECT_PATH


# pylint: disable=duplicate-code
def short_to_long(source: str) -> str:
    source_dict = {
        'both': 'Source From Both',
        'sample': 'Source From Sample Record',
        'dataset': 'Source From Dataset',
    }
    if source not in source_dict:
        raise ValueError(f"Invalid source: {source}")
    return source_dict[source]


@logger_wraps()
def add_field_project(abbrev: str, field_names: List[str]):
    field_name_objs = {"fieldAndSourceDTOs": []}
    for field_name in field_names:
        field_name_split = field_name.split(',')
        field_name_objs["fieldAndSourceDTOs"].append({
            "fieldName": field_name_split[0],
            "restrictionName": short_to_long(field_name_split[1]),
        })

    # Replace 'abbrev' with your actual value
    return api_patch(
        path=f'{PROJECT_PATH}/add-project-field/{abbrev}',
        data=field_name_objs
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
    print_formatted(
        result,
        out_format,
    )


@logger_wraps()
def remove_project_field(abbrev: str, field_names: List[str]):

    return api_patch(
        path=f'{PROJECT_PATH}/remove-project-field/{abbrev}',
        data=field_names
    )
