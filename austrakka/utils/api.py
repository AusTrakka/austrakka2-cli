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
from requests.models import Response

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

requests.packages.urllib3.disable_warnings()  # pylint: disable=no-member


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
    body: Union[Dict, List] = None,
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

    def check_failed_resp(resp: Response):
        log_dict({'Response headers': dict(resp.headers)}, logger.debug)
        try:
            resp.raise_for_status()
        except HTTPError:
            try:
                raise FailedResponseException(resp.json()) from HTTPError
            except Exception:
                raise UnknownResponseException(
                    f'Call to AusTrakka failed: {resp.reason}'
                ) from Exception

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
        raise FailedResponseException(parsed_resp)

    if method.__name__ == 'post':
        log_response(parsed_resp)

    return parsed_resp
