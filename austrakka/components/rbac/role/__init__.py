import click
from austrakka.utils.cmd_filter import hide_admin_cmds
from austrakka.utils.options import *
from austrakka.utils.output import table_format_option
from .funcs import get_roles


@click.group()
@click.pass_context
def role(ctx):
    """Commands related to role based access control"""
    ctx.context = ctx.parent.context


@role.command('get', hidden=hide_admin_cmds())
@opt_tenant_id()
@table_format_option()
def roles_get(tenant_id: str, out_format: str):
    """
    Get the list of roles defined for a tenant.
    """
    get_roles(tenant_id, out_format)
