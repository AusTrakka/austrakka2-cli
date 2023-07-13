import click
from austrakka.components.auth.enums import Auth


def opt_tenant_id(func):
    return click.option(
        '--tenant-id',
        show_envvar=True,
        required=True,
        envvar='AT_AUTH_TENANT_ID',
        help='AusTrakka tenant ID',
        default=Auth.TENANT_ID.value,
    )(func)


def opt_client_id(func):
    return click.option(
        '--client-id',
        show_envvar=True,
        required=True,
        envvar='AT_AUTH_CLIENT_ID',
        help='AusTrakka client ID',
        default=Auth.CLIENT_ID.value,
    )(func)


def opt_backend_app_uri(func):
    return click.option(
        '--app-uri',
        show_envvar=True,
        required=True,
        envvar='AT_AUTH_APP_URI',
        help='AusTrakka API URI',
        default=Auth.APP_SCOPE.value,
    )(func)
