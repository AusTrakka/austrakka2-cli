# pylint: disable=expression-not-assigned
import click

from austrakka.components.admin.message import message
from austrakka.components.admin.rawlog import rawlog
from austrakka.utils.cmd_filter import show_admin_cmds


@click.group('admin')
@click.pass_context
def admin(ctx):
    """Commands related to administration"""
    ctx.context = ctx.parent.context


admin.add_command(message) if show_admin_cmds() else None
admin.add_command(rawlog) if show_admin_cmds() else None
