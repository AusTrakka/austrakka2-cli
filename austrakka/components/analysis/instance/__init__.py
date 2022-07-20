import click

from austrakka.utils.output import table_format_option
from austrakka.components.analysis.instance.funcs import list_instances


@click.group()
@click.pass_context
def instance(ctx):
    """Commands related to analysis instances"""
    ctx.creds = ctx.parent.creds


@instance.command('list')
@table_format_option()
def analysis_list(table_format: str):
    """List analysis instances in AusTrakka"""
    list_instances(table_format)
