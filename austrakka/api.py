from typing import Callable
from typing import Dict

from loguru import logger
import requests
import click
from requests_toolbelt.multipart.encoder import MultipartEncoder

from .auth.auth_enum import Auth
from .utils import logger_wraps

get = requests.get
post = requests.post

requests.packages.urllib3.disable_warnings()  # pylint: disable=no-member

RESPONSE_TYPE_ERROR = 'Error'
RESPONSE_TYPE = 'ResponseType'

def _get_headers(content_type: str = 'application/json') -> Dict:

    token = click.get_current_context().parent.creds['token']

    return {
        'Content-Type': content_type,
        'Authorization': f'Bearer {token}',
        'Ocp-Apim-Subscription-Key': Auth.SUBSCRIPTION_KEY.value
    }


@logger_wraps()
def call_api(
    method: Callable,
    path: str,
    params: Dict = None,
    body: Dict = None,
    multipart: bool = False,
) -> Dict:
    url = f'{click.get_current_context().parent.creds["uri"]}/api/{path}'

    data = body if not multipart else MultipartEncoder(body)

    headers = _get_headers() if not isinstance(data, MultipartEncoder) \
        else _get_headers(data.content_type)

    response = method(
        url,
        headers=headers,
        verify=False,
        data=data,
        params=params,
    )

    logger.debug(f'{response.status_code} {response.reason}: {response.url}')

    parsed_resp = response.json()

    # pylint: disable=no-member
    failed = response.status_code != requests.codes.ok

    first_object = next(iter(parsed_resp), {})

    if (
        RESPONSE_TYPE in first_object
        and first_object[RESPONSE_TYPE] == RESPONSE_TYPE_ERROR
    ):
        failed = True

    if failed:
        logger.debug('Response headers:')
        for key, value in response.headers.items():
            logger.debug(f'\t{key}:{value}')
        response.raise_for_status()
        # TODO: Make an actual exception type for this
        raise Exception(f'Request failed: {first_object}')

    return response.json()
