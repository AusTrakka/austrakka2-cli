import json
from typing import Callable
from typing import Dict
from json.decoder import JSONDecodeError

from loguru import logger
import requests
import click
from requests_toolbelt.multipart.encoder import MultipartEncoder

from ..components.auth.enums import Auth
from .misc import logger_wraps
from .output import log_dict

get = requests.get
post = requests.post

requests.packages.urllib3.disable_warnings()  # pylint: disable=no-member

RESPONSE_TYPE_SUCCESS = 'Success'
RESPONSE_TYPE_ERROR = 'Error'
RESPONSE_TYPE = 'ResponseType'


class UnknownResponseException(Exception):
    pass


class FailedResponseException(Exception):
    pass


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

    if multipart:
        data = MultipartEncoder(fields=body)
    else:
        data = json.dumps(body) if body is not None else None

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

    # pylint: disable=no-member
    failed = not response.ok

    def check_failed_resp(response):
        log_dict({'Response headers': dict(response.headers)}, logger.debug)
        response.raise_for_status()

    check_failed_resp(response)

    try:
        parsed_resp = response.json()
    except JSONDecodeError as ex:
        logger.debug(str(ex))
        raise UnknownResponseException(
            f'Unable to parse response: "{response.text}"'
        ) from ex

    first_object = next(iter(parsed_resp), {})

    if (
        RESPONSE_TYPE in first_object
        and first_object[RESPONSE_TYPE] == RESPONSE_TYPE_ERROR
    ):
        failed = True

    if failed:
        check_failed_resp(response)
        # If the API returns 200 but contains a response type of error,
        # check_failed_resp will not raise an exception. Therefore this needs to
        # be here
        raise FailedResponseException(f'Request failed: {first_object}')

    if (
        RESPONSE_TYPE in first_object
        and first_object[RESPONSE_TYPE] == RESPONSE_TYPE_SUCCESS
    ):
        log_dict({'API Response': first_object}, logger.success)
    else:
        log_dict({'API Response': parsed_resp}, logger.success)

    return parsed_resp
