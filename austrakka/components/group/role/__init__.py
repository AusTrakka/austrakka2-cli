from typing import List

from austrakka.utils.output import table_format_option
from austrakka.utils.cmd_filter import hide_admin_cmds
from austrakka.utils.options import *
from .funcs import list_role, add_role, remove_role


@click.group()
@click.pass_context
def role(ctx):
    """Commands related to group role assignments"""
    ctx.context = ctx.parent.context


@role.command('list', hidden=hide_admin_cmds())
@opt_show_disabled()
@table_format_option()
def role_list(show_disabled: bool, out_format: str):
    '''
    List of role assignments for all users.
    '''
    list_role(show_disabled, out_format)


@role.command('add', hidden=hide_admin_cmds())
@opt_user_object_id()
@opt_group_role()
def role_add(
        user_id: str,
        group_role: List[str]):
    """
    Assign the user to the specified groups with the specified roles.
    """
    add_role(user_id, group_role)


@role.command('remove', hidden=hide_admin_cmds())
@opt_user_object_id()
@opt_group_role()
def role_remove(
        user_id: str,
        group_role: List[str]):
    """
    Remove the user from the specified group and role combinations.
    """
    remove_role(user_id, group_role)
