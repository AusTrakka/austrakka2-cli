import pandas as pd

from austrakka.utils.api import call_api
from austrakka.utils.api import get
from austrakka.utils.misc import logger_wraps
from austrakka.utils.output import print_table


@logger_wraps()
def print_get(path: str, table_format: str):
    response = call_api(
        method=get,
        path=path,
    )

    result = response['data'] if ('data' in response) else response
    result = pd.DataFrame.from_dict(result)

    print_table(
        result,
        table_format,
    )
