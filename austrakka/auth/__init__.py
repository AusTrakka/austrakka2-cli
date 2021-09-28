import click

from .auth import user_login
from .auth import process_login as proc_login


@click.group()
@click.pass_context
@click.help_option("-h", "--help")
def auth(ctx):
    '''Commands related to auth'''
    ctx.creds = ctx.parent.creds


@auth.command('user')
@click.help_option("-h", "--help")
def user():
    '''Get a token as a user'''
    user_login()


@auth.command('process')
@click.help_option("-h", "--help")
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
    proc_login(email, secret)
