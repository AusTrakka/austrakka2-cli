import pandas as pd
from austrakka.utils.api import call_api
from austrakka.utils.api import post, get
from austrakka.utils.helpers.output import call_get_and_print_table
from austrakka.utils.misc import logger_wraps
from austrakka.utils.paths import PROJECT_PATH
from austrakka.utils.output import print_table


@logger_wraps()
def add_project(abbrev: str, name: str, description: str):
    return call_api(
        method=post,
        path=PROJECT_PATH,
        body={
            "abbreviation": abbrev,
            "name": name,
            "description": description,
            "isActive": True
        }
    )


@logger_wraps()
def list_projects(out_format: str):
    response = call_api(
        method=get,
        path=PROJECT_PATH,
    )

    data = response['data'] if ('data' in response) else response
    result = pd.DataFrame.from_dict(data)

    drop(result, 'projectAnalyses')
    drop(result, 'projectMembers')
    drop(result, 'lastUpdated')
    drop(result, 'lastUpdatedBy')
    drop(result, 'description')

    print_table(
        result,
        out_format,
    )


def drop(data_frame, field: str):
    if field in data_frame:
        data_frame.drop([field], axis='columns', inplace=True)
