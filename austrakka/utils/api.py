import http
import json
from typing import Callable
from typing import Dict
from typing import List
from typing import Union
from json.decoder import JSONDecodeError
from http import HTTPStatus

from httpx import HTTPStatusError
import httpx

from austrakka.utils.exceptions import FailedResponseException
from austrakka.utils.exceptions import UnknownResponseException
from austrakka.utils.exceptions import UnauthorizedException
from austrakka.utils.output import log_response
from austrakka.utils.context import CxtKey
from austrakka.utils.context import get_ctx_value
from austrakka import __version__

CONTENT_TYPE_JSON = 'application/json'
CONTENT_TYPE_MULTIPART = 'multipart/form-data; charset=utf-8; boundary=+++'
WWW_AUTHENTICATE = 'www-authenticate'
INVALID_TOKEN = 'invalid_token'

def _get_default_headers(
        content_type: str = CONTENT_TYPE_JSON,
) -> Dict:
    default_headers = {
        'Content-Type': content_type,
        'Authorization': f'Bearer {get_ctx_value(CxtKey.CTX_TOKEN)}',
        'User-Agent': f'austrakka/{__version__}',
    }
    return default_headers


def _check_response(response: httpx.Response):
    # pylint: disable=raise-missing-from
    try:
        parsed_resp = response.json()
        if 'data' not in parsed_resp or 'messages' not in parsed_resp:
            raise UnknownResponseException(
                f'{response.status_code}: {parsed_resp}'
            )
        try:
            response.raise_for_status()
        except HTTPStatusError:
            raise FailedResponseException(parsed_resp, response.status_code)
    except JSONDecodeError:
        if response.status_code == http.HTTPStatus.UNAUTHORIZED:
            err = 'Unauthorized'
            auth_err = response.headers.get(WWW_AUTHENTICATE) or ''
            if INVALID_TOKEN in auth_err:
                err = 'Unauthorized: invalid or expired token'
            raise UnauthorizedException(err)
        raise UnknownResponseException(
            f'{response.status_code}: {response.text}'
        )


def _get_data(body: Union[Dict, List] = None) -> str:
    return json.dumps(body) if body is not None else None


def _get_url(path: str):
    return f'{get_ctx_value(CxtKey.CTX_URI)}/api/{path}'


def get_response(response: httpx.Response, log_resp: bool = False) -> Dict:
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
        verify=get_ctx_value(CxtKey.CTX_VERIFY_CERT),
        timeout=None,
        http2=get_ctx_value(CxtKey.CTX_USE_HTTP2),
    )


def _use_http_client(
        content_type: str = CONTENT_TYPE_JSON,
        log_resp: bool = False,
        parse_resp: bool = True
):
    def decorator(func):
        def inner_func(*args, **kwargs):
            with _get_client(content_type) as client:
                response = func(*args, **kwargs, client=client)
                if parse_resp:
                    return get_response(response, log_resp)
                return response
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
        func: Callable[[httpx.Response], None],
        params: Dict = None,
):
    """
    Throws httpx.HTTPStatusError if status is not 2xx.
    """
    if params is None:
        params = {}
    resp: httpx.Response
    with _get_client().stream("GET", _get_url(path), params=params) as resp:
        resp.raise_for_status()
        func(resp)


@_use_http_client(content_type=CONTENT_TYPE_MULTIPART, log_resp=True)
def api_post_multipart(
        path: str,
        files,
        params: Dict = None,
        data: Union[Dict, List] = None,
        custom_headers: Dict = None,
        client: httpx.Client = None,
):
    custom_headers = {} if custom_headers is None else custom_headers
    return client.post(
        _get_url(path),
        data=data,
        params=params,
        files=files,
        headers=dict(client.headers) | custom_headers
    )


@_use_http_client(content_type=CONTENT_TYPE_MULTIPART,
                  log_resp=True, parse_resp=False)
def api_post_multipart_raw(
        path: str,
        files,
        params: Dict = None,
        data: Union[Dict, List] = None,
        custom_headers: Dict = None,
        client: httpx.Client = None,
):
    custom_headers = {} if custom_headers is None else custom_headers
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
def api_post_list(
        path: str,
        params: Dict = None,
        data: List = None,
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


@_use_http_client(log_resp=True)
def api_delete(
        path: str,
        params: Dict = None,
        custom_headers: Dict = None,
        client: httpx.Client = None,
):
    return client.delete(
        _get_url(path),
        params=params,
        headers=dict(client.headers) | custom_headers
    )
