from typing import List

import pandas as pd

from austrakka.utils.api import call_api
from austrakka.utils.api import get, post
from austrakka.utils.misc import logger_wraps
from austrakka.utils.output import print_table
from austrakka.utils.paths import METADATACOLUMNTYPE_PATH


@logger_wraps()
def list_fieldtypes(table_format: str):
    response = call_api(
        method=get,
        path=METADATACOLUMNTYPE_PATH,
    )

    data = response['data'] if ('data' in response) else response
    for row in data:
        if 'validValues' in row:
            row['validValues'] = [val['name'] for val in row['validValues']]
    result = pd.DataFrame.from_dict(data)
    

    print_table(
        result,
        table_format,
    )

@logger_wraps()
def add_fieldtype(
        name: str,
        description: str,
        validValues: List[str],
):
    """
    Add a categorical fieldtype (MetaDataColumnType) and its valid values to AusTrakka.
    """
    call_api(
        method=post,
        path=METADATACOLUMNTYPE_PATH,
        body={
            "Name": name,
            "Description": description,
            "ValidValues": validValues,
            "IsActive": True
        }
    )