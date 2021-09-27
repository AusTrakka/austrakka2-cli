import click

from .auth import user_login


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
