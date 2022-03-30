from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Union

import click
import pandas as pd
from tabulate import tabulate
from loguru import logger

from austrakka.utils.enums.api import RESPONSE_TYPE
from austrakka.utils.enums.api import RESPONSE_TYPE_ERROR
from austrakka.utils.enums.api import RESPONSE_TYPE_SUCCESS
from austrakka.utils.enums.api import RESPONSE_TYPE_WARNING
from austrakka.utils.enums.api import RESPONSE_DATA
from austrakka.utils.enums.api import RESPONSE_MESSAGES
from austrakka.utils.enums.api import RESPONSE_MESSAGE


FORMAT_PREFIX = '_format_'


def _format_csv(
    dataframe: pd.DataFrame,
    headers: Union[str, List[Any]],
) -> str:
    return dataframe.to_csv(header=headers, index=False)


def _format_json(
    dataframe: pd.DataFrame,
    _,
) -> str:
    return dataframe.to_json(orient='records', date_format='iso')


def _format_pretty(
    dataframe: pd.DataFrame,
    headers: Union[str, List[Any]],
) -> str:
    return tabulate(dataframe, headers=headers, showindex=False)


def _format_html(
    dataframe: pd.DataFrame,
    headers: Union[str, List[Any]],
) -> str:
    return dataframe.to_html(header=headers, index=False)


def _format_tsv(
    dataframe: pd.DataFrame,
    headers: Union[str, List[Any]],
) -> str:
    return dataframe.to_csv(header=headers, index=False, sep='\t')


def default_format():
    return _format_pretty.__name__[len(FORMAT_PREFIX):]


def print_table(
    dataframe: pd.DataFrame,
    output_format: str = default_format(),
    print_output: bool = True,
    headers: Union[str, List[Any]] = 'keys',
):
    format_func = f'{FORMAT_PREFIX}{output_format}'

    output = globals()[format_func](dataframe, headers)

    if print_output:
        print(output)

    return output


def format_types():
    formats = []
    for key, value in globals().items():
        if (
            callable(value) and value.__module__ == __name__
            and key.startswith(FORMAT_PREFIX)
        ):
            formats.append(key[len(FORMAT_PREFIX):])
    return formats


def table_format_option():
    return click.option(
        '-f',
        '--table-format',
        default=default_format(),
        type=click.Choice(format_types()),
        help='Table formatting option',
        show_default=True,
    )


def log_dict(items: Dict, log_func: Callable, indent: int = 0) -> None:
    for key, val in items.items():
        if isinstance(val, dict):
            log_func('\t' * indent + f'{key}:')
            log_dict(val, log_func, indent + 1)
        else:
            log_func('\t' * indent + f'{key}:{val}')


def log_response(response):
    def log_item(item):
        if item[RESPONSE_TYPE] == RESPONSE_TYPE_SUCCESS:
            log_dict({item.pop(RESPONSE_TYPE): item}, logger.success)
        elif item[RESPONSE_TYPE] == RESPONSE_TYPE_WARNING:
            log_dict({item.pop(RESPONSE_TYPE): item}, logger.warning)
        elif item[RESPONSE_TYPE] == RESPONSE_TYPE_ERROR:
            log_dict({item.pop(RESPONSE_TYPE): item}, logger.error)
        else:
            log_dict({'Unknown response:': item}, logger.critical)

    if RESPONSE_MESSAGES in response:
        for item in response[RESPONSE_MESSAGES]:
            log_item(item)
    else:
        # This is to handle for legacy endpoints that don't return ApiResponse
        for item in response:
            log_item(item)
    if RESPONSE_DATA in response:
        for item in response[RESPONSE_DATA]:
            log_dict({'Inserted': item}, logger.success)


def create_response_object(message: str, message_type: str):
    return {
        RESPONSE_MESSAGE: message,
        RESPONSE_TYPE: message_type
    }
