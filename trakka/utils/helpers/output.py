from typing import Dict, Union, List
from loguru import logger

from trakka.utils.api import api_get
from trakka.utils.misc import logger_wraps
from trakka.utils.output import print_dataframe, read_pd

@logger_wraps()
def call_get_and_print(
        path: str,
        out_format: str,
        params: Dict = None,
        restricted_cols: Union[List[str], None] = None,
        datetime_cols: list[str] = None
):
    params = {} if params is None else params
    response = api_get(
        path=path,
        params=params,
    )

    result = response['data'] if ('data' in response) else response

    if not result:
        logger.info("Nothing found.")
        return
    
    print_dataframe(
        read_pd(result, out_format),
        out_format,
        restricted_cols=restricted_cols,
        datetime_cols=datetime_cols,
    )
