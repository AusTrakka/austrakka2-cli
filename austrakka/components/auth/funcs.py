import sys
from contextlib import redirect_stdout

from azure.identity import ClientSecretCredential
from azure.identity import DeviceCodeCredential
from loguru import logger

from .enums import Auth


def user_login():

    logger.warning(
        'NOTE: This may take some time to return a token after '
        + 'authenticating in the browser'
    )
    # redirecting this to stderr so DeviceCodeCredential can print the
    # azure link and code, and the user can still get the token from the
    # subprocess
    with redirect_stdout(sys.stderr):
        credential = DeviceCodeCredential(
            authority=Auth.AUTH_URL.value,
            tenant_id=Auth.TENANT_ID.value,
            client_id=Auth.CLIENT_ID.value,
        )
        credential.authenticate(scopes=[Auth.APP_SCOPE.value])
        token = credential.get_token(Auth.APP_SCOPE.value)

    # pylint: disable=print-function
    print(token.token)


def process_login(client_id: str, client_secret: str):
    credential = ClientSecretCredential(
        authority=Auth.AUTH_URL.value,
        tenant_id=Auth.TENANT_ID.value,
        client_id=client_id,
        client_secret=client_secret,
    )
    token = credential.get_token(Auth.APP_SCOPE.value)

    # pylint: disable=print-function
    print(token.token)
