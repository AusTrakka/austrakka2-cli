import pandas as pd

from ..api import call_api
from ..api import get
from ..utils import logger_wraps
from ..output import print_table

SPECIES_ROUTE = 'Species'


@logger_wraps()
def list_species(table_format: str):
    response = call_api(
        method=get,
        path=SPECIES_ROUTE,
    )

    result = pd.DataFrame.from_dict(response)

    print_table(
        result,
        table_format,
    )
