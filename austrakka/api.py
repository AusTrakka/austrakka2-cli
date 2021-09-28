from loguru import logger
import requests
import click

from .auth.auth_enum import Auth
from .utils import logger_wraps

get = requests.get
post = requests.post


requests.packages.urllib3.disable_warnings()  # pylint: disable=no-member


def _get_headers():

    token = click.get_current_context().parent.creds['token']

    return {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}',
        'Ocp-Apim-Subscription-Key': Auth.SUBSCRIPTION_KEY.value
    }


@logger_wraps()
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

    logger.debug(f'{response.status_code} {response.reason}: {response.url}')

    # pylint: disable=no-member
    if response.status_code != requests.codes.ok:
        logger.debug('Response headers:')
        for key, value in response.headers.items():
            logger.debug(f'\t{key}:{value}')
        response.raise_for_status()

    return response.json()
