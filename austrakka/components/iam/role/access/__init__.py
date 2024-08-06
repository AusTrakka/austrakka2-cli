from austrakka.components.iam.role.access.funcs import get_access, add_access, remove_access
from austrakka.utils.cmd_filter import hide_admin_cmds
from austrakka.utils.options import *
from austrakka.utils.output import table_format_option


@click.group()
@click.pass_context
def access(ctx):
    """Commands related to access definition for roles."""
    ctx.context = ctx.parent.context


@access.command('get', hidden=hide_admin_cmds())
@opt_role()
@table_format_option()
def access_get(role: str, out_format: str):
    """
    Get the list of access defined for a role.
    """
    get_access(role, out_format)


@access.command('add', hidden=hide_admin_cmds())
@opt_role()
@opt_global_ids(help="Comma separated list of scope global ids to assign to the role")
def access_add(role: str, global_ids: list[str]):
    """
    Add access to a role.
    """
    add_access(role, global_ids)


@access.command('remove', hidden=hide_admin_cmds())
@opt_scope_access_def_global_id(help="The id of the scope access definition enry to remove")
def access_remove(scope_access_def_global_id: str):
    """
    Remove access from a role.
    """
    remove_access(scope_access_def_global_id)
