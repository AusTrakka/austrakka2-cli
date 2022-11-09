# pylint: disable=expression-not-assigned
from typing import List
import click

from austrakka.utils.output import table_format_option
from austrakka.utils.cmd_filter import hide_admin_cmds, show_admin_cmds

from austrakka.components.group.field import field
from .funcs import \
    add_group, \
    update_group, \
    list_group, \
    assign_groups, \
    unassign_groups

from ...utils.options import *


@click.group()
@click.pass_context
def group(ctx):
    """Commands related to groups"""
    ctx.creds = ctx.parent.creds


group.add_command(field) if show_admin_cmds() else None


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
    help_text="The new name of the group",
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


@group.command('assign', hidden=hide_admin_cmds())
@opt_user_object_id()
@click.option('-gr',
              '--group-roles',
              help='The group and role assignment for the specified user. '
                   'Multiple assignments may be added. Use comma (,) as a separator. '
                   'Format is <group>,<role> Eg. group1,role1',
              type=click.STRING,
              multiple=True)
def group_assign(
        user_id: str,
        group_roles: List[str]):
    """
    Assign the user to the specified groups with the specified roles.
    """
    assign_groups(user_id, group_roles)


@group.command('unassign', hidden=hide_admin_cmds())
@opt_user_object_id()
@click.option('-gr',
              '--group-roles',
              help='The group and role to remove from the specified user.'
                   'Multiple assignment removals can be specified. Use comma (,) '
                   'as a separator. Format is <group>,<role> Eg. group1,role1',
              type=click.STRING,
              multiple=True)
def group_unassign(
        user_id: str,
        group_roles: List[str]):
    """
    Remove the user from the specified group and role combinations.
    """
    unassign_groups(user_id, group_roles)


@group.command('list')
@table_format_option()
def group_list(out_format: str):
    """List all known groups in AusTrakka"""
    list_group(out_format)
