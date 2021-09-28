from ..api import call_api
from ..api import get
from ..utils import logger_wraps

USER_PATH = 'Users'


@logger_wraps()
def list_users():
    response = call_api(
        method=get,
        path=USER_PATH,
        params={
            'includeall': False
        }
    )

    print(response)
