import click

from .funcs import list_privileges, assign_privilege, remove_privilege

from trakka.utils.options import (
    opt_role,
    opt_user_identifier,
    opt_identifier,
    opt_resource_type
)
from trakka.utils.output import table_format_option
from trakka.utils.cmd_filter import hide_admin_cmds


@click.group(hidden=hide_admin_cmds())
@click.pass_context
def privilege(ctx):
    """Commands related to role assignments at any level"""
    ctx.context = ctx.parent.context


@privilege.command('list',
                   help="List all privilege assignments across any entities")
@opt_resource_type(
    required=False,
    help="Only show privileges assigned to resources of the given type")
@opt_identifier( # this is -id; will this be clear to users? is there a better option?
    required=False,
    var_name="resource_id",
    help=f"Only show privileges assigned to resource with the given identifier. Resource type must also be specified.")
@opt_user_identifier(
    required=False,
    help=f"Only show privileges held by the specified user.")
@opt_role(
    required=False,
    help=f"Only show assignments of the specified role.")
@table_format_option()
def privilege_list(resource_type, resource_id, user_id, role, out_format: str):
    list_privileges(resource_type, resource_id, user_id, role, out_format)

# TODO: would we rather this (and corresponding commands) were `privilege add`?
@privilege.command('assign',
                   help="Assign a privilege to a user")
@opt_resource_type(
    required=True,
    help="Type of the resource to which access will be granted")
@opt_identifier( # this is -id; will this be clear to users? is there a better option?
    required=False,
    var_name="resource_id",
    help=f"Identifier of the resource to which access will be granted. " +
         "Must be specified unless resource type is System.")
@opt_user_identifier(
    required=True,
    help=f"Identifier of the user to whom access will be granted.")
@opt_role(
    required=True,
    help=f"Identifier of the role to be assigned.")
def privilege_assign(resource_type, resource_id, user_id, role):
    assign_privilege(resource_type, resource_id, user_id, role)


@privilege.command('remove',
                   help="Remove a privilege from a user")
@opt_resource_type(
    required=True,
    help="Type of the resource from which access will be removed")
@opt_identifier( # this is -id; will this be clear to users? is there a better option?
    required=False,
    var_name="resource_id",
    help=f"Identifier of the resource from which access will be removed. " +
         "Must be specified unless resource type is System.")
@opt_user_identifier(
    required=True,
    help=f"Identifier of the user from whom access will be removed.")
@opt_role(
    required=True,
    help=f"Identifier of the role to be unassigned.")
def privilege_remove(resource_type, resource_id, user_id, role):
    remove_privilege(resource_type, resource_id, user_id, role)