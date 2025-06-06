import click
from austrakka.components.auth.enums import Auth
from austrakka import __prog_name__ as PROG_NAME


def opt_tenant_id(func):
    return click.option(
        '--tenant-id',
        show_envvar=True,
        required=True,
        envvar='AT_AUTH_TENANT_ID',
        help=f'{PROG_NAME} tenant ID',
        default=Auth.TENANT_ID.value,
    )(func)


def opt_client_id(func):
    return click.option(
        '--client-id',
        show_envvar=True,
        required=True,
        envvar='AT_AUTH_CLIENT_ID',
        help=f'{PROG_NAME} client ID',
        default=Auth.CLIENT_ID.value,
    )(func)


def opt_backend_app_uri(func):
    return click.option(
        '--app-uri',
        show_envvar=True,
        required=True,
        envvar='AT_AUTH_APP_URI',
        help=f'{PROG_NAME} API URI',
        default=Auth.APP_SCOPE.value,
    )(func)


def opt_process_auth_id(func):
    return click.option(
        '--id',
        'process_id',
        show_envvar=True,
        required=True,
        envvar='AT_AUTH_PROCESS_ID',
        help="Process account ID"
    )(func)


def opt_process_auth_secret(func):
    return click.option(
        '--secret',
        show_envvar=True,
        required=True,
        envvar='AT_AUTH_PROCESS_SECRET',
        help='Process account secret'
    )(func)
