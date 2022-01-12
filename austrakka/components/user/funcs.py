import pandas as pd

from austrakka.utils.api import call_api
from austrakka.utils.api import get
from austrakka.utils.misc import logger_wraps
from austrakka.utils.output import print_table

USER_PATH = 'Users'


def get_users(include_all: bool = False):
    response = call_api(
        method=get,
        path=USER_PATH,
        params={
            'includeall': include_all
        }
    )

    result = pd.DataFrame.from_dict(response)
    return result


@logger_wraps()
def list_users(table_format: str):
    result = get_users()

    print_table(
        result,
        table_format,
    )
