from enum import Enum

from click import get_current_context


class CxtKey(Enum):
    CTX_URI = 'uri'
    CTX_TOKEN = 'token'
    CTX_VERIFY_CERT = 'verify_cert'
    CTX_USE_HTTP2 = 'use_http2'


def get_ctx_value(ctx_key: CxtKey):
    return get_current_context().parent.context[ctx_key.value]
