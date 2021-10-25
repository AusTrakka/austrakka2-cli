import pandas as pd

from ..api import call_api
from ..api import get
from ..utils import logger_wraps
from ..output import print_table

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
