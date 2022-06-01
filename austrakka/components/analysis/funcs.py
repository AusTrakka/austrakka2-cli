import pandas as pd

from austrakka.utils.api import call_api
from austrakka.utils.api import get
from austrakka.utils.misc import logger_wraps
from austrakka.utils.output import print_table
from austrakka.utils.paths import ANALYSIS_PATH


@logger_wraps()
def list_analyses(table_format: str):
    response = call_api(
        method=get,
        path=ANALYSIS_PATH,
    )

    result = response['data'] if ('data' in response) else response
    result = pd.DataFrame.from_dict(result)

    print_table(
        result,
        table_format,
    )
