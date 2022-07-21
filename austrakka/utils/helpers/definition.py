from austrakka.utils.api import call_api
from austrakka.utils.api import get
from austrakka.utils.paths import JOB_DEFINITION_PATH


def get_definition_by_name(name: str):
    response = call_api(
        method=get,
        path=f"{JOB_DEFINITION_PATH}/name/{name}"
    )
    return response['data'] if ('data' in response) else response
