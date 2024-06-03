import cgi

import httpx


# pylint: disable=too-few-public-methods
class HEADERS:
    CONTENT_DISPOSITION = 'Content-Disposition'


def get_header(resp: httpx.Response, header_name: str) -> str:
    header = resp.headers.get(header_name)
    if not header:
        raise ValueError(f"{header_name} header not found in response")
    return header


def parse_header(resp: httpx.Response, header_name: str) -> tuple[str, dict[str, str]]:
    header = get_header(resp, header_name)
    return cgi.parse_header(header)


def get_header_value(resp: httpx.Response, header_name: str, value_name: str) -> str:
    _, params = parse_header(resp, header_name)
    try:
        return params[value_name]
    except KeyError as ex:
        raise ValueError(f"Value {value_name} not found for header {header_name}") from ex
