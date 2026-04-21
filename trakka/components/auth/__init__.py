import click

from .funcs import user_login
from .funcs import process_login
from .opts import opt_tenant_id
from .opts import opt_client_id
from .opts import opt_backend_app_uri
from .opts import opt_process_auth_id
from .opts import opt_process_auth_secret


@click.group('auth')
@click.pass_context
def auth(ctx):
    '''Commands related to auth'''
    ctx.context = ctx.parent.context


@auth.command('user')
@opt_tenant_id
@opt_client_id
@opt_backend_app_uri
def user(
        tenant_id: str,
        client_id: str,
        app_uri: str
):
    '''Get a token as a user'''
    user_login(tenant_id, client_id, app_uri)


@auth.command('process')
@opt_tenant_id
@opt_backend_app_uri
@opt_process_auth_id
@opt_process_auth_secret
def process(
        tenant_id: str,
        app_uri: str,
        process_id: str,
        secret: str
):
    '''Get a token as a process'''
    process_login(tenant_id, app_uri, process_id, secret)
