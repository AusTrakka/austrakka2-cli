import click

from austrakka.components.activity.funcs import get_activity
from austrakka.utils.cmd_filter import hide_admin_cmds
from austrakka.utils.output import table_format_option


@click.group()
@click.pass_context
def activity(ctx):
    """Commands related to platform activity log"""
    ctx.context = ctx.parent.context

@activity.command('get', hidden=hide_admin_cmds())
@table_format_option()
def activity_get(out_format: str):
    get_activity(out_format)