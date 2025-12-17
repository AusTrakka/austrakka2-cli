from typing import Union
import click

from austrakka.components.iam.privilege.funcs import (
    list_privileges,
    list_by_role_privileges,
    list_by_user_privileges,
    assign_privilege,
    unassign_privilege)

from austrakka.utils.privilege import TENANT_RESOURCE
from austrakka.utils.cmd_filter import hide_admin_cmds
from austrakka.utils.options import (
    opt_global_id,
    opt_record_type,
    opt_role,
    opt_user_object_id,
    opt_user_global_id)

from austrakka.utils.output import table_format_option

GLOBAL_ID_HELP="Global ID. Required for non-tenant"

@click.group()
@click.pass_context
def privilege(ctx):
    """Commands related to already assigned privileges"""
    ctx.context = ctx.parent.context


# pylint: disable=duplicate-code
@privilege.command('list', hidden=hide_admin_cmds())
@opt_record_type(default=TENANT_RESOURCE)
@opt_global_id(
    required=False,
    default=None,
    help=GLOBAL_ID_HELP,
)
@table_format_option()
def privilege_list(record_type: str, global_id: str, out_format: str):
    """
    List all privileges assigned to a record
    """
    validate_global_id(record_type, global_id)
    list_privileges(record_type, global_id, out_format)


@privilege.command('list-by-role', hidden=hide_admin_cmds())
@opt_role()
@opt_record_type(default=TENANT_RESOURCE)
@opt_global_id(
    required=False,
    default=None,
    help=GLOBAL_ID_HELP,
)
@table_format_option()
def privilege_list_by_role(role: str, record_type: str, global_id: str, out_format: str):
    """
    List the privileges assigned to a record for a specific role
    """
    validate_global_id(record_type, global_id)
    list_by_role_privileges(role, record_type, global_id, out_format)


@privilege.command('list-by-user', hidden=hide_admin_cmds())
@opt_user_object_id()
@opt_record_type(default=TENANT_RESOURCE)
@opt_global_id(
    required=False,
    default=None,
    help=GLOBAL_ID_HELP,
)
@table_format_option()
def privilege_list_by_user(user_id: str, record_type: str, global_id: str, out_format: str):
    """
    List the privileges assigned to a record for a specific user
    """
    validate_global_id(record_type, global_id)
    list_by_user_privileges(user_id, record_type, global_id, out_format)


@privilege.command('assign', hidden=hide_admin_cmds())
@opt_user_global_id()
@opt_role()
@opt_global_id(
    required=False,
    default=None,
    help=GLOBAL_ID_HELP,
)
@opt_record_type(default=TENANT_RESOURCE)
def privilege_assign(
        user_global_id: str,
        role: str,
        global_id: str,
        record_type: str):
    """
    Assign privileges to access a record by a user
    """
    validate_global_id(record_type, global_id)
    assign_privilege(user_global_id, role, global_id, record_type)


@privilege.command('unassign', hidden=hide_admin_cmds())
@opt_global_id(
    required=False,
    default=None,
    help=GLOBAL_ID_HELP,
)
@opt_record_type(default=TENANT_RESOURCE)
@click.argument('privilege-global-id', type=str)
def privilege_unassign(
        global_id: str,
        record_type: str,
        privilege_global_id: str):
    """
    Remove privileges to access a record from a user
    """
    validate_global_id(record_type, global_id)
    unassign_privilege(global_id, record_type, privilege_global_id)


def validate_global_id(record_type: str, global_id: Union[str, None]):
    if record_type == TENANT_RESOURCE and global_id is not None:
        raise ValueError("Cannot provide global id with Tenant")
    if record_type != TENANT_RESOURCE and global_id is None:
        raise ValueError("Must provide global id")
