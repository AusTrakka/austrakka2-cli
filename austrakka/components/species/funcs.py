import pandas as pd

from austrakka.utils.api import call_api
from austrakka.utils.api import get
from austrakka.utils.misc import logger_wraps
from austrakka.utils.output import print_table

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
