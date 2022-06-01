import pandas as pd
from loguru import logger
from os import path

from loguru import logger

from austrakka.utils.helpers.fields import get_fieldtype_by_name

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
    result = pd.DataFrame.from_dict(data)

    # TODO flag to show validvalues for categorical fields

    print_table(
        result,
        table_format,
    )
