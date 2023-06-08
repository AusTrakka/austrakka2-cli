# pylint: disable=expression-not-assigned
import click

from austrakka.components.dashboard.proj import proj
from austrakka.utils.cmd_filter import show_admin_cmds


@click.group()
@click.pass_context
def dashboard(ctx):
    """Commands related to defining a dashboard."""
    ctx.context = ctx.parent.context


dashboard.add_command(proj) if show_admin_cmds() else None
