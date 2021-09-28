import requests
import click

from .auth.auth_enum import Auth

get = requests.get
post = requests.post


def _get_headers():

    token = click.get_current_context().parent.creds['token']

    return {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}',
        'Ocp-Apim-Subscription-Key': Auth.SUBSCRIPTION_KEY.value
    }


def call_api(
    method: str,
    path: str,
    params: dict = None,
    body: dict = None,
):
    url = f'{click.get_current_context().parent.creds["uri"]}/api/{path}'

    response = method(
        url,
        headers=_get_headers(),
        verify=False,
        data=body,
        params=params,
    )

    # pylint: disable=no-member
    if response.status_code != requests.codes.ok:
        response.raise_for_status()

    return response.json()
