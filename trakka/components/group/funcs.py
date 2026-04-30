from loguru import logger

from trakka.utils.api import api_get
from trakka.utils.api import api_post
from trakka.utils.api import api_put
from trakka.utils.helpers.groups import format_group_dto_for_output
from trakka.utils.misc import logger_wraps
from trakka.utils.paths import GROUP_PATH


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

    api_put(
        path=f'{GROUP_PATH}/{name}',
        data=payload)

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

    return api_post(
        path=GROUP_PATH,
        data=payload)


@logger_wraps()
def list_group(out_format: str):
    response = api_get(
        path=GROUP_PATH,
    )

    data = response['data'] if ('data' in response) else response
    format_group_dto_for_output(data, out_format)
