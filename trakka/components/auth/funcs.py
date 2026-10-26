import sys
from contextlib import redirect_stdout

from azure.identity import ClientSecretCredential
from azure.identity import DeviceCodeCredential
from loguru import logger

from trakka.utils.config import get_server_info
from trakka.utils.context import CxtKey
from trakka.utils.context import TrakkaCxt


def _get_api_scope(app_uri):
    return f'{app_uri}/.default'


def user_login():
    (client_id, tenant_id, app_uri, _) = get_server_info(
        TrakkaCxt.get_value(CxtKey.URI),
        TrakkaCxt.get_value(CxtKey.SKIP_CERT_VERIFY),
    )

    app_scope = _get_api_scope(app_uri)
    logger.warning(
        'NOTE: This may take some time to return a token after '
        + 'authenticating in the browser'
    )
    # redirecting this to stderr so DeviceCodeCredential can print the
    # azure link and code, and the user can still get the token from the
    # subprocess
    with redirect_stdout(sys.stderr):
        credential = DeviceCodeCredential(
            tenant_id=tenant_id,
            client_id=client_id,
        )
        credential.authenticate(scopes=[app_scope])
        token = credential.get_token(app_scope)

    # pylint: disable=bad-builtin
    print(token.token)


def process_login(
        process_id: str,
        client_secret: str
):
    (_, tenant_id, app_uri, _) = get_server_info(
        TrakkaCxt.get_value(CxtKey.URI),
        TrakkaCxt.get_value(CxtKey.SKIP_CERT_VERIFY),
    )

    credential = ClientSecretCredential(
        tenant_id=tenant_id,
        client_id=process_id,
        client_secret=client_secret,
    )
    log_token_info(credential, app_uri)
    token = credential.get_token(_get_api_scope(app_uri))

    # pylint: disable=bad-builtin
    print(token.token)


def log_token_info(credential: ClientSecretCredential, app_uri: str):
    token_info = credential.get_token_info(_get_api_scope(app_uri))
    token_info_dict = token_info.__dict__
    if 'token' in token_info_dict: 
        del token_info_dict['token']
    logger.info(token_info_dict)
