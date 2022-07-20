from austrakka.utils.api import call_api, call_get_and_print_table
from austrakka.utils.api import post
from austrakka.utils.misc import logger_wraps
from austrakka.utils.paths import PROJECT_PATH


@logger_wraps()
def add_project(abbrev: str, name: str, description: str, org: str):
    return call_api(
        method=post,
        path=PROJECT_PATH,
        body={
            "abbreviation": abbrev,
            "name": name,
            "description": description,
            "owningOrganisation": {
                "abbreviation": org
            }
        }
    )


@logger_wraps()
def list_projects(table_format: str):
    call_get_and_print_table(PROJECT_PATH, table_format)
