import json
from typing import Dict
from typing import List
from typing import Union
from json.decoder import JSONDecodeError

import click
from httpx import HTTPStatusError
import httpx

from austrakka.utils.exceptions import FailedResponseException
from austrakka.utils.exceptions import UnknownResponseException
from austrakka.components.auth.enums import Auth
from austrakka.utils.output import log_response

NO_CONTENT = 204
TIMEOUT_IN_SECONDS = 300

CONTENT_TYPE_JSON = 'application/json'
CONTENT_TYPE_MULTIPART = 'multipart/form-data; charset=utf-8; boundary=+++'


def _get_headers(
        content_type: str = CONTENT_TYPE_JSON,
        custom_headers: Dict = None,
) -> Dict:
    custom_headers = custom_headers if custom_headers else {}
    token = click.get_current_context().parent.creds['token']
    default_headers = {
        'Content-Type': content_type,
        'Authorization': f'Bearer {token}',
        'Ocp-Apim-Subscription-Key': Auth.SUBSCRIPTION_KEY.value
    }
    return default_headers | custom_headers


def _check_response(response: httpx.Response):
    # pylint: disable=raise-missing-from
    try:
        response.raise_for_status()
    except HTTPStatusError as http_error:
        try:
            parsed_resp = response.json()
            if 'data' not in parsed_resp or 'messages' not in parsed_resp:
                raise UnknownResponseException(parsed_resp)
            raise FailedResponseException(parsed_resp)
        except JSONDecodeError:
            raise http_error


def _get_data(body: Union[Dict, List] = None) -> str:
    return json.dumps(body) if body is not None else None


def _get_url(path: str):
    return f'{click.get_current_context().parent.creds["uri"]}/api/{path}'


def _get_response(response: httpx.Response, log_resp: bool = False) -> Dict:
    _check_response(response)
    parsed_resp = {} if response.status_code == NO_CONTENT else response.json()
    if log_resp:
        log_response(parsed_resp)
    return parsed_resp


def api_get(
        path: str,
        params: Dict = None,
):
    headers = _get_headers()
    response = httpx.get(
        _get_url(path),
        headers=headers,
        verify=False,
        params=params,
        timeout=TIMEOUT_IN_SECONDS,
    )
    return _get_response(response)


def api_get_stream(
        path: str,
):
    headers = _get_headers()
    return httpx.stream(
        "GET",
        _get_url(path),
        headers=headers,
        verify=False,
        timeout=TIMEOUT_IN_SECONDS,
    )


def api_post_multipart(
        path: str,
        files,
        params: Dict = None,
        data: Union[Dict, List] = None,
        custom_headers: Dict = None,
):
    headers = _get_headers(CONTENT_TYPE_MULTIPART, custom_headers)
    response = httpx.post(
        _get_url(path),
        headers=headers,
        verify=False,
        data=data,
        params=params,
        files=files,
        timeout=TIMEOUT_IN_SECONDS,
    )
    return _get_response(response, log_resp=True)


def api_post(
        path: str,
        params: Dict = None,
        data: Union[Dict, List] = None,
):
    headers = _get_headers()
    response = httpx.post(
        _get_url(path),
        headers=headers,
        verify=False,
        data=json.dumps(data),
        params=params,
        timeout=TIMEOUT_IN_SECONDS,
    )
    return _get_response(response, log_resp=True)


def api_put(
        path: str,
        params: Dict = None,
        data: Union[Dict, List] = None,
):
    headers = _get_headers()
    response = httpx.put(
        _get_url(path),
        headers=headers,
        verify=False,
        data=json.dumps(data),
        params=params,
        timeout=TIMEOUT_IN_SECONDS,
    )
    return _get_response(response, log_resp=True)


def api_patch(
        path: str,
        params: Dict = None,
        data: Union[Dict, List] = None,
):
    headers = _get_headers()
    response = httpx.patch(
        _get_url(path),
        headers=headers,
        verify=False,
        data=json.dumps(data),
        params=params,
        timeout=TIMEOUT_IN_SECONDS,
    )
    return _get_response(response, log_resp=True)
