# pylint: disable=expression-not-assigned
import click

from trakka.components.dashboard.project import project
from trakka.utils.cmd_filter import show_admin_cmds


@click.group()
@click.pass_context
def dashboard(ctx):
    """Commands related to defining a dashboard"""
    ctx.context = ctx.parent.context


dashboard.add_command(project) if show_admin_cmds() else None
