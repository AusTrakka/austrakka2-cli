from os import path
from austrakka.utils.api import api_post
from austrakka.utils.api import api_patch
from austrakka.utils.helpers.output import call_get_and_print_table
from austrakka.utils.misc import logger_wraps
from austrakka.utils.paths import PROJECT_PATH

SET_DASHBOARD = 'set-dashboard'


@logger_wraps()
def add_project(abbrev: str, name: str, description: str, org: str, dashboard_name: str):
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
def set_dashboard(project_id: int, dashboard_name: str):
    return api_patch(
        path=path.join(PROJECT_PATH, SET_DASHBOARD, str(project_id)),
        data=dashboard_name
    )


@logger_wraps()
def list_projects(out_format: str):
    call_get_and_print_table(PROJECT_PATH, out_format)
