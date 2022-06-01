from os import path

import pandas as pd

from austrakka.utils.api import call_api
from austrakka.utils.api import get, post
from austrakka.utils.misc import logger_wraps
from austrakka.utils.output import print_table

SPECIES_PATH = 'Species'
SPECIES_DTO = 'dto'


@logger_wraps()
def add_species(abbrev: str, name: str, taxon_id: str):
    return call_api(
        method=post,
        path=SPECIES_PATH,
        body={
            "abbreviation": abbrev,
            "name": name,
            "taxonId": taxon_id
        }
    )


@logger_wraps()
def list_species(table_format: str):
    response = call_api(
        method=get,
        path=path.join(SPECIES_PATH, SPECIES_DTO),
    )

    data = response['data'] if ('data' in response) else response
    result = pd.DataFrame.from_dict(data)

    print_table(
        result,
        table_format,
    )
