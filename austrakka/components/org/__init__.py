import click

from austrakka.utils.output import table_format_option
from .funcs import list_orgs


@click.group()
@click.pass_context
def org(ctx):
    '''Commands related to organisations'''
    ctx.creds = ctx.parent.creds


@org.command('list')
@table_format_option()
def org_list(table_format: str):
    '''List organisations in AusTrakka'''
    list_orgs(table_format)
