import click

from trakka.utils.options import (
    opt_role,
    opt_user_identifier,
    opt_identifier,
    opt_resource_type
)
from trakka.utils.output import table_format_option
from trakka.utils.cmd_filter import hide_admin_cmds

from .funcs import list_privileges


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
    help="Only show privileges assigned to resource with the given identifier." + 
         "Resource type must also be specified.")
@opt_user_identifier(
    required=False,
    help="Only show privileges held by the specified user.")
@opt_role(
    required=False,
    help="Only show assignments of the specified role.")
@table_format_option()
def privilege_list(resource_type, resource_id, user_id, role, out_format: str):
    list_privileges(resource_type, resource_id, user_id, role, out_format)
