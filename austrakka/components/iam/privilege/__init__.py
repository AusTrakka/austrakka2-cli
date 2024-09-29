import click

from austrakka.components.iam.privilege.funcs import (
    list_privileges,
    list_by_role_privileges,
    list_by_user_privileges,
    assign_privilege,
    unassign_privilege)

from austrakka.utils.privilege import convert_record_type_to_route_string
from austrakka.utils.cmd_filter import hide_admin_cmds
from austrakka.utils.options import (
    opt_record_type,
    opt_role,
    opt_user_object_id,
    opt_record_global_id)

from austrakka.utils.output import table_format_option


@click.group()
@click.pass_context
def privilege(ctx):
    """Commands related to already assigned privileges"""
    ctx.context = ctx.parent.context


@privilege.command('list', hidden=hide_admin_cmds())
@opt_record_type()
@click.argument('record-global-id', type=str)
@table_format_option()
def privilege_list(record_type: str, record_global_id: str, out_format: str):
    """
    List all privileges assigned to a record
    """
    record_type_route = convert_record_type_to_route_string(record_type)
    list_privileges(record_type_route, record_global_id, out_format)


@privilege.command('list-by-role', hidden=hide_admin_cmds())
@opt_role()
@opt_record_type()
@click.argument('record-global-id', type=str)
@table_format_option()
def privilege_list_by_role(role: str, record_type: str, record_global_id: str, out_format: str):
    """
    List the privileges assigned to a record for a specific role
    """
    record_type_route = convert_record_type_to_route_string(record_type)
    list_by_role_privileges(role, record_type_route, record_global_id, out_format)


@privilege.command('list-by-user', hidden=hide_admin_cmds())
@opt_user_object_id()
@opt_record_type()
@click.argument('record-id', type=str)
@table_format_option()
def privilege_list_by_user(user_id: str, record_type: str, record_id: str, out_format: str):
    """
    List the privileges assigned to a record for a specific user
    """
    record_type_route = convert_record_type_to_route_string(record_type)
    list_by_user_privileges(user_id, record_type_route, record_id, out_format)


@privilege.command('assign', hidden=hide_admin_cmds())
@opt_user_object_id()
@opt_role()
@opt_record_global_id()
@opt_record_type()
def privilege_assign(
        user_id: str,
        role: str,
        record_global_id: str,
        record_type: str):
    """
    Assign privileges to access a record by a user
    """
    record_type_route = convert_record_type_to_route_string(record_type)
    assign_privilege(user_id, role, record_global_id, record_type_route)


@privilege.command('unassign', hidden=hide_admin_cmds())
@opt_record_global_id()
@opt_record_type()
@click.argument('privilege-global-id', type=str)
def privilege_unassign(
        record_global_id: str,
        record_type: str,
        privilege_global_id: str):
    """
    Remove privileges to access a record from a user
    """
    record_type_route = convert_record_type_to_route_string(record_type)
    unassign_privilege(record_global_id, record_type_route, privilege_global_id)
