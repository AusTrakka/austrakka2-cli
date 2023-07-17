import sys
from contextlib import redirect_stdout

from azure.identity import ClientSecretCredential
from azure.identity import DeviceCodeCredential
from loguru import logger


def _get_api_scope(app_uri):
    return f'{app_uri}/.default'


def user_login(
        tenant_id: str,
        client_id: str,
        app_uri: str,
):
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

    # pylint: disable=print-function
    print(token.token)


def process_login(
        tenant_id: str,
        app_uri: str,
        process_id: str,
        client_secret: str
):
    credential = ClientSecretCredential(
        tenant_id=tenant_id,
        client_id=process_id,
        client_secret=client_secret,
    )
    token = credential.get_token(_get_api_scope(app_uri))

    # pylint: disable=print-function
    print(token.token)
