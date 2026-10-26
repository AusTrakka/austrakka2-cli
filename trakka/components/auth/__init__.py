import click

from .funcs import user_login
from .funcs import process_login
from .opts import opt_process_auth_id
from .opts import opt_process_auth_secret


@click.group('auth')
@click.pass_context
def auth(ctx):
    '''Commands related to auth'''
    ctx.context = ctx.parent.context


@auth.command('user')
def user():
    '''Get a token as a user'''
    user_login()


@auth.command('process')
@opt_process_auth_id
@opt_process_auth_secret
def process(
        process_id: str,
        secret: str
):
    '''Get a token as a process'''
    process_login(process_id, secret)
