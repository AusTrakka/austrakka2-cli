from austrakka.components.iam.role.definition.funcs import (
    get_role_definition,
    add_role_definition,
    remove_role_definition)

from austrakka.utils.cmd_filter import hide_admin_cmds
from austrakka.utils.options import *
from austrakka.utils.output import table_format_option


@click.group()
@click.pass_context
def definition(ctx):
    """Commands related to access definition for roles."""
    ctx.context = ctx.parent.context


@definition.command('get', hidden=hide_admin_cmds())
@opt_role()
@opt_view_type()
@table_format_option()
def role_access_get(role: str, view_type: str, out_format: str):
    """
    Get the list of scope access definition for a role.
    """
    get_role_definition(role, view_type, out_format)


@definition.command('add', hidden=hide_admin_cmds())
@opt_role()
@opt_global_ids(help="Comma separated list of scope global ids to assign to the role")
def role_definition_add(role: str, global_ids: list[str]):
    """
    Add scope access definition to a role.
    """
    add_role_definition(role, global_ids)


@definition.command('remove', hidden=hide_admin_cmds())
@opt_scope_access_def_global_id(help="The id of the scope access definition enry to remove")
def role_definition_remove(scope_access_def_global_id: str):
    """
    Remove scope access definition from a role.
    """
    remove_role_definition(scope_access_def_global_id)
