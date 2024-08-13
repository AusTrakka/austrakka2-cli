import pandas as pd

from austrakka.utils.api import api_get
from austrakka.utils.misc import logger_wraps
from austrakka.utils.output import print_dataframe


# pylint: disable=expression-not-assigned,duplicate-code
@logger_wraps()
def get_default_tenant(out_format: str):
    """
    Get the default tenant.
    """
    response = api_get(path="v2/tenant/default")
    data = response['data'] if ('data' in response) else response
    result = pd.json_normalize(data, max_level=1)

    print_dataframe(
        result,
        out_format,
    )
