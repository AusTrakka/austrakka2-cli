# pylint: disable=duplicate-code

from loguru import logger

from austrakka.utils.api import api_post
from austrakka.utils.api import api_patch
from austrakka.utils.api import api_put
from austrakka.utils.helpers.output import call_get_and_print
from austrakka.utils.helpers.project import get_project_by_abbrev
from austrakka.utils.misc import logger_wraps
from austrakka.utils.paths import PROJECT_PATH
from austrakka.utils.paths import SET_DASHBOARD
from austrakka.utils.paths import DASHBOARD_WIDGETS
from austrakka.utils.paths import PROJECT_SETTINGS

@logger_wraps()
def add_project(
        abbrev: str,
        name: str,
        description: str,
        org: str,
        dashboard_name: str):
    return api_post(
        path=PROJECT_PATH,
        data={
            "abbreviation": abbrev,
            "name": name,
            "description": description,
            "isActive": True,
            "requestingOrg": {
                "abbreviation": org
            },
            "dashboardName": dashboard_name
        }
    )


@logger_wraps()
def update_project(
        project_abbreviation: str,
        abbrev: str,
        name: str,
        description: str,
        is_active: bool,
        org: str,
        dashboard_name: str):
    project = get_project_by_abbrev(project_abbreviation)

    # ProjectDTO fields which should go in ProjectPutDTO
    put_project = {k: project[k] for k in [
        'abbreviation',
        'name',
        'description',
        'isActive',
        'requestingOrg',
        'dashboardName'
    ]}
    if project['requestingOrg'] is None:
        put_project['requestingOrg'] = {'abbreviation': None}

    if abbrev is not None:
        logger.warning(f"Updating project abbreviation from {project['abbreviation']} to {abbrev}")
        put_project['abbreviation'] = abbrev
    if name is not None:
        put_project['name'] = name
    if description is not None:
        put_project['description'] = description
    if is_active is not None:
        put_project['isActive'] = is_active
    if org is not None:
        put_project['requestingOrg'] = {
            "abbreviation": org
        }
    if dashboard_name is not None:
        put_project['dashboardName'] = dashboard_name

    return api_put(
        path=f"{PROJECT_PATH}/{project_abbreviation}",
        data=put_project
    )

@logger_wraps()
def set_dashboard(project_id: int, dashboard_name: str):
    return api_patch(
        path='/'.join([PROJECT_PATH, SET_DASHBOARD, str(project_id)]),
        data=dashboard_name
    )


@logger_wraps()
def list_projects(out_format: str):
    call_get_and_print(PROJECT_PATH, out_format)


@logger_wraps()
def get_dashboard(project_id: int, out_format: str):
    joined_path = '/'.join([PROJECT_PATH, DASHBOARD_WIDGETS, str(project_id)])
    call_get_and_print(joined_path, out_format)

@logger_wraps()
def show_project_settings(abbrev: str, out_format: str):
    path = '/'.join([PROJECT_PATH, abbrev, PROJECT_SETTINGS])
    call_get_and_print(path, out_format)
    