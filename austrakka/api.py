import requests

import click


get = requests.get
post = requests.post


def _get_headers():

    token = click.get_current_context().parent.creds['token']
    sub_key = click.get_current_context().parent.creds['api_key']

    return {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}',
        'Ocp-Apim-Subscription-Key': sub_key
    }


def call_api(method: str, path: str, body: dict = None):
    url = f'{click.get_current_context().parent.creds["uri"]}/api/{path}'

    response = method(
        url,
        headers=_get_headers(),
        verify=False,
        data=body,
    )

    # TODO: this needs to handle incorrect tokens and displaying an appropriate
    # message to the user

    print(response.content)

    return response.content
