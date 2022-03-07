from os import path

import pandas as pd

from austrakka.utils.api import call_api
from austrakka.utils.api import get
from austrakka.utils.misc import logger_wraps
from austrakka.utils.output import print_table

SPECIES_PATH = 'Species'
SPECIES_DTO = 'dto'

@logger_wraps()
def list_species(table_format: str):
    response = call_api(
        method=get,
        path=path.join(SPECIES_PATH, SPECIES_DTO),
    )

    result = pd.DataFrame.from_dict(response)

    print_table(
        result,
        table_format,
    )
