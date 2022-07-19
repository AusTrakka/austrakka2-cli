from austrakka.utils.api import call_api
from austrakka.utils.api import get
from austrakka.utils.paths import USER_PATH


def get_user_by_email(email: str):
    response = call_api(
        method=get,
        path=f"{USER_PATH}/email/{email}"
    )
    return response['data'] if ('data' in response) else response
