import httpx


# pylint: disable=too-few-public-methods
class HEADERS:
    CONTENT_DISPOSITION = 'Content-Disposition'


def get_header(resp: httpx.Response, header_name: str) -> str:
    header = resp.headers.get(header_name)
    if not header:
        raise ValueError(f"{header_name} header not found in response")
    return header


def get_header_value(resp: httpx.Response, header_name: str, value_name: str) -> str:
    header = get_header(resp, header_name)
    _, params = parse_header(header)
    try:
        return params[value_name]
    except KeyError as ex:
        raise ValueError(f"Value {value_name} not found for header {header_name}") from ex

# Taken from Python sourcecode after cgi removal: https://github.com/python/cpython/blob/3.11/Lib/cgi.py#L238
def _parseparam(s):
    while s[:1] == ';':
        s = s[1:]
        end = s.find(';')
        while end > 0 and (s.count('"', 0, end) - s.count('\\"', 0, end)) % 2:
            end = s.find(';', end + 1)
        if end < 0:
            end = len(s)
        f = s[:end]
        yield f.strip()
        s = s[end:]

def parse_header(line):
    """Parse a Content-type like header.
    Return the main content-type and a dictionary of options.
    """
    parts = _parseparam(';' + line)
    key = parts.__next__()
    pdict = {}
    for p in parts:
        i = p.find('=')
        if i >= 0:
            name = p[:i].strip().lower()
            value = p[i+1:].strip()
            if len(value) >= 2 and value[0] == value[-1] == '"':
                value = value[1:-1]
                value = value.replace('\\\\', '\\').replace('\\"', '"')
            pdict[name] = value
    return key, pdict
