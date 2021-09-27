import click

from .user import list_users


@click.group()
@click.pass_context
@click.help_option("-h", "--help")
def user(ctx):
    '''Commands related to users'''
    ctx.creds = ctx.parent.creds


@user.command('list')
@click.help_option("-h", "--help")
def user_list():
    '''List users in AusTrakka'''
    list_users()
