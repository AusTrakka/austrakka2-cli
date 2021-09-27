from ..api import call_api
from ..api import get

USER_PATH = 'Users'


def list_users():
    call_api(
        get,
        f'{USER_PATH}?includeall=false'
    )
