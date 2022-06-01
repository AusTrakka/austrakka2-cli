import pandas as pd

from austrakka.utils.api import call_api
from austrakka.utils.api import get
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

    print_table(
        result,
        table_format,
    )
