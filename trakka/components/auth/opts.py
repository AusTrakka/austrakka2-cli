import click
from trakka.components.auth.enums import Auth
from trakka.utils.context import CxtKey, TrakkaCxt


def opt_tenant_id(func):
    return click.option(
        '--tenant-id',
        show_envvar=True,
        required=True,
        envvar=TrakkaCxt.get_env_var_names(CxtKey.AUTH_TENANT_ID),
        help='Tenant ID',
        default=Auth.TENANT_ID.value,
    )(func)


def opt_client_id(func):
    return click.option(
        '--client-id',
        show_envvar=True,
        required=True,
        envvar=TrakkaCxt.get_env_var_names(CxtKey.AUTH_CLIENT_ID),
        help='Client ID',
        default=Auth.CLIENT_ID.value,
    )(func)


def opt_backend_app_uri(func):
    return click.option(
        '--app-uri',
        show_envvar=True,
        required=True,
        envvar=TrakkaCxt.get_env_var_names(CxtKey.AUTH_APP_URI),
        help='API URI',
        default=Auth.APP_SCOPE.value,
    )(func)


def opt_process_auth_id(func):
    return click.option(
        '--id',
        'process_id',
        show_envvar=True,
        required=True,
        envvar=TrakkaCxt.get_env_var_names(CxtKey.AUTH_PROCESS_ID),
        help="Process account ID"
    )(func)


def opt_process_auth_secret(func):
    return click.option(
        '--secret',
        show_envvar=True,
        required=True,
        envvar=TrakkaCxt.get_env_var_names(CxtKey.AUTH_PROCESS_SECRET),
        help='Process account secret'
    )(func)
