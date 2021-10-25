import click

from .analysis import list_analyses
from ..output import table_format_option


@click.group()
@click.pass_context
def analysis(ctx):
    '''Commands related to analyses'''
    ctx.creds = ctx.parent.creds


@analysis.command('list')
@table_format_option()
def analysis_list(table_format: str):
    '''List analyses in AusTrakka'''
    list_analyses(table_format)
