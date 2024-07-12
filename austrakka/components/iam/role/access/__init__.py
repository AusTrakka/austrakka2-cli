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
@opt_tenant_id()
@opt_role()
@table_format_option()
def access_get(tenant_id: str, role: str, out_format: str):
    """
    Get the list of access defined for a role.
    """
    get_access(tenant_id, role, out_format)


@access.command('add', hidden=hide_admin_cmds())
@opt_tenant_id()
@opt_role()
@opt_ids(help="Comma separated list of scope ids to assign to the role")
def access_add(tenant_id: str, role: str, ids: list[int]):
    """
    Add access to a role.
    """
    add_access(tenant_id, role, ids)


@access.command('remove', hidden=hide_admin_cmds())
@opt_tenant_id()
@opt_scope_access_def_id(help="The id of the scope access definition enry to remove")
def access_remove(tenant_id: str, scope_access_def_id: int):
    """
    Remove access from a role.
    """
    remove_access(tenant_id, scope_access_def_id)
