import pandas as pd

from austrakka.utils.api import call_api, get
from austrakka.utils.misc import logger_wraps
from austrakka.utils.output import print_table


@logger_wraps()
def call_get_and_print_table(path: str, out_format: str):
    response = call_api(
        method=get,
        path=path,
    )

    result = response['data'] if ('data' in response) else response
    result = pd.json_normalize(result, max_level=1)

    print_table(
        result,
        out_format,
    )
