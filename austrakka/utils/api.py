import json
from typing import Callable
from typing import Dict
from typing import List
from typing import Union
from json.decoder import JSONDecodeError

from loguru import logger
import requests
import click
from requests_toolbelt.multipart.encoder import MultipartEncoder
from requests.exceptions import HTTPError

from austrakka.utils.enums.api import RESPONSE_TYPE
from austrakka.utils.enums.api import RESPONSE_TYPE_ERROR
from austrakka.utils.exceptions import FailedResponseException
from austrakka.utils.exceptions import UnknownResponseException
from ..components.auth.enums import Auth
from .misc import logger_wraps
from .output import log_dict
from .output import log_response

get = requests.get
post = requests.post
put = requests.put
patch = requests.patch

NO_CONTENT = 204
TIMEOUT_IN_SECONDS = 300

requests.packages.urllib3.disable_warnings()  # pylint: disable=no-member


def _get_headers(content_type: str = 'application/json') -> Dict:

    token = click.get_current_context().parent.creds['token']

    return {
        'Content-Type': content_type,
        'Authorization': f'Bearer {token}',
        'Ocp-Apim-Subscription-Key': Auth.SUBSCRIPTION_KEY.value
    }


@logger_wraps()
# pylint: disable=too-many-arguments
def call_api(
    method: Callable,
    path: str,
    params: Dict = None,
    body: Union[Dict, List] = None,
    multipart: bool = False,
    custom_headers: Dict = None,
) -> Dict:
    url = f'{click.get_current_context().parent.creds["uri"]}/api/{path}'

    if multipart:
        data = MultipartEncoder(fields=body)
    else:
        data = json.dumps(body) if body is not None else None

    headers = _get_headers() if not isinstance(data, MultipartEncoder) \
        else _get_headers(data.content_type)
    custom_headers = custom_headers if custom_headers else {}
    headers = headers | custom_headers

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

    log_dict({'Response headers': dict(response.headers)}, logger.debug)
    try:
        response.raise_for_status()
    except HTTPError as http_error:
        try:
            if not hasattr(response.json(), "data") \
                    or not hasattr(response.json(), "messages"):
                raise UnknownResponseException(response.json()) from HTTPError
            raise FailedResponseException(response.json()) from HTTPError
        except FailedResponseException as ex:
            raise ex from ex
        except JSONDecodeError:
            # pylint: disable=raise-missing-from
            raise http_error
    parsed_resp = {} if response.status_code == NO_CONTENT else response.json()
    first_object = next(iter(parsed_resp), {})

    if (
        RESPONSE_TYPE in first_object
        and first_object[RESPONSE_TYPE] == RESPONSE_TYPE_ERROR
    ):
        failed = True

    if failed:
        raise FailedResponseException(parsed_resp)

    try:
        if method.__name__ in ('post', 'put'):
            log_response(parsed_resp)
    except TypeError as ex:
        raise UnknownResponseException(f'Unknown response: {response.text}')\
            from ex

    return parsed_resp


@logger_wraps()
# pylint: disable=too-many-arguments
def call_get_api(
    path: str,
    params: Dict = None,
) -> Dict:
    url = f'{click.get_current_context().parent.creds["uri"]}/api/{path}'

    response = get(
        url,
        headers=_get_headers(),
        verify=False,
        params=params,
        timeout=TIMEOUT_IN_SECONDS,
    )
    ensure_success_status(response)

    json_obj = json.loads(response.text)
    return json_obj['data']


def ensure_success_status(response):
    try:
        response.raise_for_status()
    except HTTPError as http_error:
        try:
            raise FailedResponseException(response.json()) from HTTPError
        except FailedResponseException as ex:
            raise ex from ex
        except JSONDecodeError:
            # pylint: disable=raise-missing-from
            raise http_error


@logger_wraps()
# pylint: disable=too-many-arguments
def call_api_raw(
        path: str,
        params: Dict = None,
        stream: bool = False,
):
    url = f'{click.get_current_context().parent.creds["uri"]}/api/{path}'

    response = get(
        url,
        headers=_get_headers(),
        verify=False,
        params=params,
        stream=stream,
        timeout=TIMEOUT_IN_SECONDS,
    )

    ensure_success_status(response)

    return response
