from typing import Callable
from typing import Dict
from typing import List
from typing import Union

import click
import pandas as pd
from pandas import DataFrame
from tabulate import tabulate
from loguru import logger

from austrakka.utils.datetimes import dt_format_and_convert
from austrakka.utils.enums.api import RESPONSE_TYPE
from austrakka.utils.enums.api import RESPONSE_TYPE_ERROR
from austrakka.utils.enums.api import RESPONSE_TYPE_SUCCESS
from austrakka.utils.enums.api import RESPONSE_TYPE_WARNING
from austrakka.utils.enums.api import RESPONSE_DATA
from austrakka.utils.enums.api import RESPONSE_MESSAGES
from austrakka.utils.enums.api import RESPONSE_MESSAGE
from austrakka.utils.enums.view_type import COMPACT, MORE, FULL

_FORMAT_PREFIX = '_format_'
_EXTENSION_PREFIX = '_extension_'

DEFAULT_DATETIME_COLUMNS = ['created', 'lastUpdated', 'eventTime']

# pylint: disable=too-few-public-methods
class FORMATS:
    PRETTY = 'pretty'
    CSV = 'csv'
    JSON = 'json'
    HTML = 'html'
    TSV = 'tsv'


def _extension_csv():
    return "csv"


def _extension_json():
    return "json"


def _extension_pretty():
    return "out"


def _extension_html():
    return "html"


def _extension_tsv():
    return "tsv"


def _format_csv(
        dataframe: pd.DataFrame,
) -> str:
    return dataframe.to_csv(index=False)


def _format_json(
        dataframe: pd.DataFrame,
) -> str:
    return dataframe.to_json(
        orient='records',
        date_format='iso',
        indent=2) + "\n"


def _format_pretty(
        dataframe: pd.DataFrame,
) -> str:
    return tabulate(dataframe, showindex=False) + "\n"


def _format_html(
        dataframe: pd.DataFrame,
) -> str:
    return dataframe.to_html(index=False) + "\n"


def _format_tsv(
        dataframe: pd.DataFrame,
) -> str:
    return dataframe.to_csv(index=False, sep='\t')


def default_table_format():
    return FORMATS.PRETTY


def default_object_format():
    return FORMATS.JSON


def print_dataframe(
        dataframe: pd.DataFrame,
        output_format: str = default_object_format(),
        restricted_cols: List[str] = None,
        timezone: str = None,
        datetime_cols: List[str] = None,
):
    datetime_cols = DEFAULT_DATETIME_COLUMNS if datetime_cols is None else datetime_cols
    
    if output_format in object_format_types():
        restricted_cols = None
    
    if restricted_cols:
        # Preserve column order
        dataframe = dataframe[[c for c in dataframe.columns if c in restricted_cols]]

    if timezone:
        for col in datetime_cols:
            if col in dataframe.columns:
                dataframe[col] = dt_format_and_convert(dataframe[col], timezone)

    output = convert_format(dataframe, output_format)

    # pylint: disable=bad-builtin
    print(output, end='')


def print_dict(
        data: dict,
        output_format: str = default_object_format(),
):
    print_dataframe(_create_dataframe(data), output_format)

def convert_format(
        dataframe: pd.DataFrame,
        output_format: str = default_object_format(),
):
    format_func = f'{_FORMAT_PREFIX}{output_format}'
    return globals()[format_func](dataframe)


def _get_output_extension(output_format: str):
    format_func = f'{_EXTENSION_PREFIX}{output_format}'
    return globals()[format_func]()


def _create_dataframe(
        data: dict
) -> pd.DataFrame:
    return pd.DataFrame.from_dict(data, dtype=object)


def write_dataframe(
        dataframe: pd.DataFrame,
        base_filepath: str,
        output_format: str = default_object_format(),
):
    """
    :param dataframe:
    :param output_format:
    :param base_filepath: Should NOT include an extension.
    """
    output = convert_format(dataframe, output_format)
    extension = _get_output_extension(output_format)
    filename = base_filepath + "." + extension
    with open(filename, "w", encoding="utf-8") as file:
        file.write(output)
    logger.info(f"Written file {filename}")


def write_dict(
        data: dict,
        base_filepath: str,
        output_format: str = default_object_format(),
):
    """
    :param data:
    :param output_format:
    :param base_filepath: Should NOT include an extension.
    """
    write_dataframe(_create_dataframe(data), base_filepath, output_format)


def table_format_types():
    formats = []
    for key, value in FORMATS.__dict__.items():
        if not key.startswith("__"):
            formats.append(value)
    return formats


def object_format_types():
    return [FORMATS.JSON, FORMATS.HTML]


def table_format_option(default: str = default_table_format()):
    return _generic_format_option(default, table_format_types())


def object_format_option(default: str = default_object_format()):
    return _generic_format_option(default, object_format_types())


def _generic_format_option(default: str, valid_formats: List[str]):
    if default not in valid_formats:
        raise ValueError(f"{default} not a valid format")
    return click.option(
        '-f',
        '--format',
        'out_format',
        default=default,
        type=click.Choice(valid_formats),
        help='Formatting option',
        show_default=True,
    )


def log_dict(items: Dict, log_func: Callable, indent: int = 0) -> None:
    for key, val in items.items():
        if isinstance(val, dict):
            log_func(' ' * (indent * 4) + f'{key}:')
            log_dict(val, log_func, indent + 1)
        else:
            log_func(' ' * (indent * 4) + f'{key}:{val}')


def log_response_compact(response):
    def log_item_compact(item):
        if item[RESPONSE_TYPE] == RESPONSE_TYPE_SUCCESS:
            logger.success(item[RESPONSE_MESSAGE])
        elif item[RESPONSE_TYPE] == RESPONSE_TYPE_WARNING:
            logger.warning(item[RESPONSE_MESSAGE])
        elif item[RESPONSE_TYPE] == RESPONSE_TYPE_ERROR:
            logger.error(item[RESPONSE_MESSAGE])
        else:
            logger.critical(item[RESPONSE_MESSAGE])

    if RESPONSE_MESSAGES in response:
        for msg in response[RESPONSE_MESSAGES]:
            log_item_compact(msg)
    else:
        # This is to handle for legacy endpoints that don't return ApiResponse
        for msg in response:
            log_item_compact(msg)


def log_response(response):
    if not response:
        return

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
    if RESPONSE_DATA in response and response[RESPONSE_DATA] is not None:
        if isinstance(response[RESPONSE_DATA], dict):
            log_dict({'Inserted': response[RESPONSE_DATA]}, logger.success)
        else:
            for item in response[RESPONSE_DATA]:
                log_dict({'Inserted': item}, logger.success)


def create_response_object(message: str, message_type: str):
    return {
        RESPONSE_MESSAGE: message,
        RESPONSE_TYPE: message_type
    }

def get_viewtype_columns(
        view_type: str,
        compact_fields: list[str],
        more_fields: list[str]
) -> Union[List[str], None]:
    if view_type == COMPACT:
        return compact_fields
    if view_type == MORE:
        return list(set(compact_fields + more_fields))
    
    assert view_type == FULL
    return None


def read_pd(data, out_format: str) -> DataFrame:
    max_level = -1 if out_format in object_format_types() else 9999
    return pd.json_normalize(data, max_level=max_level)
