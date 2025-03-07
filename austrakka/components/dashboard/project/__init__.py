import click

from austrakka.utils.output import table_format_option
from austrakka.utils.cmd_filter import hide_admin_cmds
from austrakka.components.dashboard.project.funcs import add_dashboard
from austrakka.components.dashboard.project.funcs import update_dashboard
from austrakka.components.dashboard.project.funcs import list_dashboards
from austrakka.components.dashboard.project.funcs import rename_dashboard
from ....utils.options import *


# pylint: disable=duplicate-code
@click.group()
@click.pass_context
def project(ctx):
    """Commands related to defining a project dashboard"""
    ctx.context = ctx.parent.context


@project.command('add', hidden=hide_admin_cmds())
@opt_name(help="Dashboard name. Must be unique.")
def dashboard_add(name: str):
    """Define a project dashboard"""
    add_dashboard(name)


@project.command('update', hidden=hide_admin_cmds())
@opt_name(help="Dashboard name. Must be unique.")
@click.argument('dashboard-id', type=int)
def dashboard_update(dashboard_id: int, name: str):
    """Update a project dashboard definition"""
    update_dashboard(dashboard_id, name)


@project.command('list', hidden=hide_admin_cmds())
@table_format_option()
def dashboards_list(out_format: str):
    """List project dashboards available for use in a given project"""
    list_dashboards(out_format)


@project.command('rename', hidden=hide_admin_cmds())
@click.argument('dashboard-id', type=int)
@opt_new_name(help="New name of dashoard.", )
def dashboard_rename(dashboard_id: int, new_name: str):
    """Rename a project dashboard"""
    rename_dashboard(dashboard_id, new_name)
