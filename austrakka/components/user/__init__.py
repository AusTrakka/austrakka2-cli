import click

from austrakka.utils.output import table_format_option
from .funcs import list_users


@click.group()
@click.pass_context
def user(ctx):
    '''Commands related to users'''
    ctx.creds = ctx.parent.creds


@user.command('list')
@table_format_option()
def user_list(table_format: str):
    '''List users in AusTrakka'''
    list_users(table_format)
