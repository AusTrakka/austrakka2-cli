from contextlib import redirect_stdout
import sys

import requests
from azure.identity import DeviceCodeCredential
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
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
            redirect_uri=Auth.REDIRECT_URI.value,
        )
        credential.authenticate(scopes=[Auth.APP_ID.value])
        token = credential.get_token(Auth.APP_ID.value)

    # pylint: disable=print-function
    print(token.token)


def process_login(username: str, secret_name: str):
    credential = DefaultAzureCredential()
    client = SecretClient(
        vault_url=Auth.KEY_VAULT_URI.value,
        credential=credential
    )

    retrieved_secret = client.get_secret(secret_name)

    request_payload = {
        "username": username,
        "password": retrieved_secret.value,
        "scope": Auth.APP_ID.value,
        "grant_type": "password",
        "client_id": Auth.CLIENT_ID.value
    }

    # pylint: disable=print-function,missing-timeout
    print(requests.post(
        url=f'{Auth.AUTH_URL.value}/{Auth.TENANT_ID.value}/oauth2/v2.0/token',
        data=request_payload).json()["access_token"]
    )
