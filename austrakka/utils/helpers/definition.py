from austrakka.utils.api import api_get
from austrakka.utils.paths import JOB_DEFINITION_PATH


def get_definition_by_name(name: str):
    response = api_get(
        path=f"{JOB_DEFINITION_PATH}/{name}"
    )
    return response['data'] if ('data' in response) else response
