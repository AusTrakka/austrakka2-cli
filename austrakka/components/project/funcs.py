from austrakka.utils.api import api_post
from austrakka.utils.helpers.output import call_get_and_print_table
from austrakka.utils.misc import logger_wraps
from austrakka.utils.paths import PROJECT_PATH


@logger_wraps()
def add_project(abbrev: str, name: str, description: str):
    return api_post(
        path=PROJECT_PATH,
        data={
            "abbreviation": abbrev,
            "name": name,
            "description": description,
            "isActive": True
        }
    )


@logger_wraps()
def list_projects(out_format: str):
    call_get_and_print_table(PROJECT_PATH, out_format)
