import pandas as pd

from ..api import call_api
from ..api import get
from ..utils import logger_wraps
from ..output import print_table

ANALYSIS_PATH = 'Analyses'


@logger_wraps()
def list_analyses(table_format: str):
    response = call_api(
        method=get,
        path=ANALYSIS_PATH,
    )

    result = pd.DataFrame.from_dict(response)

    print_table(
        result,
        table_format,
    )
