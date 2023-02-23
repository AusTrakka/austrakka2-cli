import click

from .funcs import user_login
from .funcs import process_login
from .enums import Auth
from .opts import opt_tenant_id
from .opts import opt_client_id
from .opts import opt_env


@click.group('auth')
@click.pass_context
def auth(ctx):
    '''Commands related to auth'''
    ctx.creds = ctx.parent.creds


@auth.command('user')
@opt_tenant_id
@opt_client_id
@opt_env
def user(tenant_id: str, client_id: str, env: str):
    '''Get a token as a user'''
    user_login(tenant_id, client_id, env)


@auth.command('process')
@opt_tenant_id
@opt_env
@click.option(
    '--id',
    'process_id',
    show_envvar=True,
    required=True,
    envvar='AT_AUTH_PROCESS_ID',
    help="Process account ID"
)
@click.option(
    '--secret',
    show_envvar=True,
    required=True,
    envvar='AT_AUTH_PROCESS_SECRET',
    help='Process account secret'
)
def process(
        tenant_id: str,
        env: str,
        process_id: str,
        secret: str
):
    '''Get a token as a process'''
    process_login(tenant_id, env, process_id, secret)
