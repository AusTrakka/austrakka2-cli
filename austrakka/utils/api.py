import json
from typing import Dict
from typing import List
from typing import Union
from json.decoder import JSONDecodeError
from http import HTTPStatus

import click
from httpx import HTTPStatusError
import httpx

from austrakka.utils.exceptions import FailedResponseException
from austrakka.utils.exceptions import UnknownResponseException
from austrakka.components.auth.enums import Auth
from austrakka.utils.output import log_response

TIMEOUT_IN_SECONDS = 300

CONTENT_TYPE_JSON = 'application/json'
CONTENT_TYPE_MULTIPART = 'multipart/form-data; charset=utf-8; boundary=+++'


def _get_default_headers(
        content_type: str = CONTENT_TYPE_JSON,
) -> Dict:
    token = click.get_current_context().parent.context['token']
    default_headers = {
        'Content-Type': content_type,
        'Authorization': f'Bearer {token}',
        'Ocp-Apim-Subscription-Key': Auth.SUBSCRIPTION_KEY.value
    }
    return default_headers


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
    return f'{click.get_current_context().parent.context["uri"]}/api/{path}'


def _get_response(response: httpx.Response, log_resp: bool = False) -> Dict:
    _check_response(response)
    parsed_resp = {} \
        if response.status_code == HTTPStatus.NO_CONTENT else response.json()
    if log_resp:
        log_response(parsed_resp)
    return parsed_resp


def _get_client(
        content_type: str = CONTENT_TYPE_JSON
):
    return httpx.Client(
        headers=_get_default_headers(content_type),
        verify=click.get_current_context().parent.context['verify_cert'],
        timeout=TIMEOUT_IN_SECONDS,
    )


def _use_http_client(
        content_type: str = CONTENT_TYPE_JSON,
        log_resp: bool = False,
):
    def decorator(func):
        def inner_func(*args, **kwargs):
            with _get_client(content_type) as client:
                response = func(*args, **kwargs, client=client)
                return _get_response(response, log_resp)
        return inner_func
    return decorator


@_use_http_client()
def api_get(
        path: str,
        params: Dict = None,
        client: httpx.Client = None,
):
    return client.get(
        _get_url(path),
        params=params,
    )


def api_get_stream(
        path: str,
):
    return _get_client().stream(
        "GET",
        _get_url(path),
    )


@_use_http_client(content_type=CONTENT_TYPE_MULTIPART, log_resp=True)
def api_post_multipart(
        path: str,
        files,
        params: Dict = None,
        data: Union[Dict, List] = None,
        custom_headers: Dict = None,
        client: httpx.Client = None,
):
    return client.post(
        _get_url(path),
        data=data,
        params=params,
        files=files,
        headers=dict(client.headers) | custom_headers
    )


@_use_http_client(log_resp=True)
def api_post(
        path: str,
        params: Dict = None,
        data: Union[Dict, List] = None,
        client: httpx.Client = None,
):
    return client.post(
        _get_url(path),
        data=json.dumps(data),
        params=params,
    )


@_use_http_client(log_resp=True)
def api_put(
        path: str,
        params: Dict = None,
        data: Union[Dict, List] = None,
        client: httpx.Client = None,
):
    return client.put(
        _get_url(path),
        data=json.dumps(data),
        params=params,
    )


@_use_http_client(log_resp=True)
def api_patch(
        path: str,
        params: Dict = None,
        data: Union[Dict, List] = None,
        client: httpx.Client = None,
):
    return client.patch(
        _get_url(path),
        data=json.dumps(data),
        params=params,
    )
