import click
from austrakka.utils.cmd_filter import hide_admin_cmds
from austrakka.utils.options import *
from austrakka.utils.output import table_format_option
from .funcs import get_scope


@click.group()
@click.pass_context
def scope(ctx):
    """Commands related to scopes for associating with roles."""
    ctx.context = ctx.parent.context


@scope.command('get', hidden=hide_admin_cmds())
@opt_tenant_id()
@table_format_option()
def scope_get(tenant_id: str, out_format: str):
    """
    Get the list of scopes defined for a tenant.
    """
    get_scope(tenant_id, out_format)