import click

from .funcs import user_login
from .funcs import process_login


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
def process(process_id, secret):
    '''Get a token as a process'''
    process_login(process_id, secret)
