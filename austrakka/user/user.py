from ..api import call_api
from ..api import get

USER_PATH = 'Users'


def list_users():
    response = call_api(
        method=get,
        path=USER_PATH,
        params={
            'includeall': False
        }
    )

    print(response)
