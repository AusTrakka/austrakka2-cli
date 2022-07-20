import click

from austrakka.utils.output import table_format_option
from austrakka.components.analysis.definition import definition
from austrakka.components.analysis.instance import instance
from .funcs import list_analyses
from ...utils.cmd_filter import show_admin_cmds


@click.group()
@click.pass_context
def analysis(ctx):
    '''Commands related to analyses'''
    ctx.creds = ctx.parent.creds


analysis.add_command(definition) if show_admin_cmds() else None
analysis.add_command(instance) if show_admin_cmds() else None


@analysis.command('list')
@table_format_option()
def analysis_list(table_format: str):
    '''List analyses in AusTrakka'''
    list_analyses(table_format)
