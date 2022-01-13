import click

from austrakka.utils.output import table_format_option
from .funcs import list_projects


@click.group()
@click.pass_context
def project(ctx):
    '''Commands related to projects'''
    ctx.creds = ctx.parent.creds


@project.command('list')
@table_format_option()
def projects_list(table_format: str):
    '''List projects in AusTrakka'''
    list_projects(table_format)
