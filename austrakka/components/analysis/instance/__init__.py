import click

from austrakka.utils.cmd_filter import hide_admin_cmds
from austrakka.utils.output import table_format_option
from austrakka.components.analysis.instance.funcs import list_instances


@click.group()
@click.pass_context
def instance(ctx):
    """Commands related to analysis instances"""
    ctx.creds = ctx.parent.creds


@instance.command('list', hidden=hide_admin_cmds())
@table_format_option()
def analysis_list(out_format: str):
    """List analysis instances in AusTrakka"""
    list_instances(out_format)
