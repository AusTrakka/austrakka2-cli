# pylint: disable=expression-not-assigned
import click

from austrakka.components.dashboard.project import project
from austrakka.utils.cmd_filter import show_admin_cmds


@click.group()
@click.pass_context
def dashboard(ctx):
    """Commands related to defining a dashboard."""
    ctx.context = ctx.parent.context


dashboard.add_command(project) if show_admin_cmds() else None
