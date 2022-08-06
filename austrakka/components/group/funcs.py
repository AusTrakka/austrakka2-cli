import pandas as pd
from loguru import logger

from austrakka.utils.api import call_api
from austrakka.utils.api import get, post, put
from austrakka.utils.misc import logger_wraps
from austrakka.utils.output import print_table
from austrakka.utils.paths import GROUP_PATH


@logger_wraps()
def update_group(
        name: str,
        newname: str,
        org: str):

    payload = {}

    if newname:
        payload["name"] = newname

    if org:
        payload["organisation"] = {"abbreviation": org}

    call_api(
        method=put,
        path=f'{GROUP_PATH}/{name}',
        body=payload)

    logger.info('Done.')


@logger_wraps()
def add_group(
        name: str,
        org: str):

    payload = {
        "name": name,
    }

    if org:
        payload["organisation"] = {"abbreviation": org}

    return call_api(
        method=post,
        path=GROUP_PATH,
        body=payload)


@logger_wraps()
def list_group(table_format: str):
    response = call_api(
        method=get,
        path=GROUP_PATH,
    )

    data = response['data'] if ('data' in response) else response
    result = pd.json_normalize(data, max_level=1)

    result.drop(['organisation'],
                axis='columns',
                inplace=True)

    result.fillna('', inplace=True)

    print_table(
        result,
        table_format,
    )
