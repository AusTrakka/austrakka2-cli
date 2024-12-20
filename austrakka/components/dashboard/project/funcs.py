from austrakka.utils.helpers.output import call_get_and_print
from austrakka.utils.api import api_post
from austrakka.utils.api import api_put
from austrakka.utils.api import api_patch
from austrakka.utils.misc import logger_wraps
from austrakka.utils.paths import PROJECT_DASHBOARD_PATH

RENAME = 'rename'


@logger_wraps()
def add_dashboard(name: str):
    """
    Add a dashboard for use in a project.
    """
    payload = {
        "name": name,
    }

    api_post(
        path=PROJECT_DASHBOARD_PATH,
        data=payload
    )


@logger_wraps()
def update_dashboard(dashboard_id: int, name: str):
    """
    Update a dashboard definition for use in a project.
    """
    payload = {
        "name": name,
    }

    api_put(
        path=f'{PROJECT_DASHBOARD_PATH}/{dashboard_id}',
        data=payload
    )


@logger_wraps()
def list_dashboards(out_format: str):
    """
    List dashboards available for use in a project.
    """
    call_get_and_print(PROJECT_DASHBOARD_PATH, out_format)


@logger_wraps()
def rename_dashboard(dashboard_id: int, new_name: str):
    """
    Rename a dashboard.
    """
    api_patch(
        path=f'{PROJECT_DASHBOARD_PATH}/{RENAME}/{dashboard_id}',
        data=new_name
    )
