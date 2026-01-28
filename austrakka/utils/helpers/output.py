from typing import Dict
from loguru import logger

import pandas as pd

from austrakka.utils.api import api_get
from austrakka.utils.misc import logger_wraps
from austrakka.utils.output import print_dataframe, read_pd
from austrakka.utils.output import print_dataframe_viewtype


@logger_wraps()
def call_get_and_print(path: str, out_format: str, params: Dict = None):
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
    )

@logger_wraps()
def call_get_and_print_view_type(
        path: str, 
        view_type: str,
        compact_fields: list[str],
        more_fields: list[str],
        out_format: str, 
        params: Dict = None,
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
    
    # pylint: disable-next=duplicate-code
    print_dataframe_viewtype(
        read_pd(result, out_format),
        view_type,
        compact_fields,
        more_fields,
        out_format,
    )


def call_get_and_print_dataset_status(path: str,
                                      out_format: str,
                                      params: Dict = None):
    params = {} if params is None else params
    response = api_get(
        path=path,
        params=params,
    )

    result = response['data'] if ('data' in response) else response
    result = read_pd(result, out_format) \
        .pipe(lambda x: x.drop('serverSha256', axis=1))

    print_dataframe(
        result,
        out_format,
    )


@logger_wraps()
def call_get_and_print_table_on_state_change(path: str,
                                             out_format: str,
                                             prev_state: str,
                                             params: Dict = None):
    params = {} if params is None else params
    response = api_get(
        path=path,
        params=params,
    )

    result = response['data'] if ('data' in response) else response
    if result['status'] != prev_state:
        new_state = result['status']
        result = read_pd(result, out_format) \
            .pipe(lambda x: x.drop('serverSha256', axis=1))
        print_dataframe(
            result,
            out_format,
        )
        return new_state
    return None
