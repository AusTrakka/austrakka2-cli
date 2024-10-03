import click

from austrakka.components.iam.tenant.funcs import get_default_tenant
from austrakka.utils.cmd_filter import hide_admin_cmds
from austrakka.utils.output import table_format_option


@click.group()
@click.pass_context
def tenant(ctx):
    """Commands related to tenant information"""
    ctx.context = ctx.parent.context


@tenant.command('get-default', hidden=hide_admin_cmds())
@table_format_option()
def tenant_get_default(out_format: str):
    """
    Get the list of scopes defined for a tenant
    """
    get_default_tenant(out_format)
