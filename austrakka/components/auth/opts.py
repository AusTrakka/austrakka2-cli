import click
from .enums import Auth
from austrakka.utils.enums.envs import PROD


def opt_tenant_id(func):
    return click.option(
        '--tenant-id',
        show_envvar=True,
        required=True,
        default=Auth.TENANT_ID.value,
        envvar='AT_AUTH_TENANT_ID',
        help='AusTrakka tenant ID'
    )(func)


def opt_client_id(func):
    return click.option(
        '--client-id',
        show_envvar=True,
        required=True,
        default=Auth.CLIENT_ID.value,
        envvar='AT_AUTH_CLIENT_ID',
        help='AusTrakka client ID'
    )(func)


def opt_env(func):
    return click.option(
        '--env',
        show_envvar=True,
        required=True,
        default=PROD,
        envvar='AT_AUTH_ENV',
        help='AusTrakka env ID'
    )(func)
