import pandas as pd

from austrakka.utils.api import call_api
from austrakka.utils.api import get
from austrakka.utils.misc import logger_wraps
from austrakka.utils.output import print_table

USER_PATH = 'Users'


@logger_wraps()
def list_users(table_format: str):
    response = call_api(
        method=get,
        path=USER_PATH,
        params={
            'includeall': False
        }
    )

    result = pd.DataFrame.from_dict(response)

    print_table(
        result,
        table_format,
    )
