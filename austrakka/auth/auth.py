import requests
from azure.identity import InteractiveBrowserCredential
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

from .auth_enum import Auth


def user_login():
    credential = InteractiveBrowserCredential(
        authority=Auth.AUTH_URL.value,
        tenant_id=Auth.TENANT_ID.value,
        client_id=Auth.CLIENT_ID.value,
        redirect_uri=Auth.REDIRECT_URI.value,
    )
    credential.authenticate(scopes=[Auth.APP_ID.value])
    token = credential.get_token(Auth.APP_ID.value)

    print(getattr(token, 'token'))

# TODO: for logging in with a service principal


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

    print(requests.post(
        url=f'{Auth.AUTH_URL.value}/{Auth.TENANT_ID.value}/oauth2/v2.0/token',
        data=request_payload).json()["access_token"]
    )
