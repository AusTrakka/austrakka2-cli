from typing import List
from trakka.utils.api import api_get, api_patch
from trakka.utils.misc import logger_wraps
from trakka.utils.output import print_dict
from trakka.utils.paths import PROJECT_PATH


@logger_wraps()
def get_project_organisation_list(identifier: str, out_format: str):
    uri = f'{PROJECT_PATH}/{identifier}/organisations'
    response = api_get(uri)
    data = response.get('data', response)

    print_dict(data, out_format)

@logger_wraps()
def add_project_organisation(identifier: str, org: List[str]):
    uri = f'{PROJECT_PATH}/{identifier}/organisations/add'
    payload = {"organisationNames": list(org)}

    return api_patch(path=uri, data=payload)

@logger_wraps()
def remove_project_organisation(identifier: str, org: List[str]):
    uri = f'{PROJECT_PATH}/{identifier}/organisations/remove'
    payload = {"organisationNames": list(org)}

    return api_patch(path=uri, data=payload)
