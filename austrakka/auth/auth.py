from azure.identity import InteractiveBrowserCredential
from .auth_enum import Auth


def user_login():
    credential = InteractiveBrowserCredential(
        authority = Auth.AUTHORITY.value,
        tenant_id = Auth.TENANT_ID.value,
        client_id = Auth.CLIENT_ID.value,
        redirect_uri = Auth.REDIRECT_URI.value,
    )
    record = credential.authenticate(scopes=[Auth.APP_ID.value])
    token = credential.get_token(Auth.APP_ID.value)

    print(getattr(token, 'token'))

# TODO: for logging in with a service principal
def process_login():
    pass

