import pandas as pd

from austrakka.utils.api import call_api
from austrakka.utils.api import get, post
from austrakka.utils.misc import logger_wraps
from austrakka.utils.output import print_table
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
    response = call_api(
        method=get,
        path=PROJECT_PATH,
    )

    result = pd.DataFrame.from_dict(response)

    print_table(
        result,
        table_format,
    )
