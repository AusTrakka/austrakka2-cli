import click

from .funcs import user_login
from .funcs import process_login


@click.group('auth')
@click.pass_context
def auth(ctx):
    '''Commands related to auth'''
    ctx.creds = ctx.parent.creds


@auth.command('user')
def user():
    '''Get a token as a user'''
    user_login()


@auth.command('process')
@click.option(
    "--email",
    show_envvar=True,
    required=True,
    help="Process user's email"
)
@click.option(
    "--secret",
    show_envvar=True,
    required=True,
    help="Process user's secret name"
)
def process(email, secret):
    '''Get a token as a process'''
    process_login(email, secret)
