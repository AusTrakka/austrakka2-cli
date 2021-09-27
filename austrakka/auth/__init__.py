import click

from .auth import user_login
from .auth import process_login as proc_login
from ..utils import click_option


@click.group()
@click.pass_context
@click.help_option("-h", "--help")
def auth(ctx):
    '''Commands related to auth'''
    ctx.creds = ctx.parent.creds


@auth.command('login')
@click.help_option("-h", "--help")
def login():
    '''Get a token as a user'''
    user_login()


@auth.command('process-login')
@click.help_option("-h", "--help")
@click_option(
    "--process-email",
    envvar='AUSTRAKKA_PROCESS_EMAIL',
    required=True,
    help="Process user's email. Optionally can use AUSTRAKKA_PROCESS_EMAIL env var"
)
@click_option(
    "--process-secret",
    envvar='AUSTRAKKA_PROCESS_SECRET',
    required=True,
    help="Process user's secret name. Optionally can use AUSTRAKKA_PROCESS_SECRET env var"
)
def process_login(process_email, process_secret):
    '''Get a token as a process'''
    proc_login(process_email, process_secret)
