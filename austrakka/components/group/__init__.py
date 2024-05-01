# pylint: disable=expression-not-assigned
import click

from austrakka.components.group.field import field
from austrakka.components.group.funcs import add_group
from austrakka.components.group.funcs import list_group
from austrakka.components.group.funcs import update_group
from austrakka.components.group.role import role
from austrakka.utils.cmd_filter import hide_admin_cmds, show_admin_cmds
from austrakka.utils.options import opt_name
from austrakka.utils.options import opt_organisation
from austrakka.utils.output import table_format_option


@click.group()
@click.pass_context
def group(ctx):
    """Commands related to groups"""
    ctx.context = ctx.parent.context


group.add_command(field) if show_admin_cmds() else None
group.add_command(role) if show_admin_cmds() else None


@group.command('add', hidden=hide_admin_cmds())
@opt_name()
@opt_organisation(required=False)
def group_add(
        name: str,
        org):
    """
    Add a new group to the given organisation.
    """
    add_group(name, org)


@group.command('update', hidden=hide_admin_cmds())
@click.argument('name', type=str)
@opt_name(
    help="The new name of the group",
    required=False,
    var_name='newname'
)
@opt_organisation(required=False)
def group_update(
        name: str,
        newname: str,
        org: str):
    """
    Update a group name or organisation.
    """
    update_group(
        name,
        newname,
        org)


@group.command('list')
@table_format_option()
def group_list(out_format: str):
    """List all known groups in AusTrakka"""
    list_group(out_format)
