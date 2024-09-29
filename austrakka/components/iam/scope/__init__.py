from austrakka.utils.cmd_filter import hide_admin_cmds
from austrakka.utils.options import *
from austrakka.utils.output import table_format_option
from .funcs import list_scopes


@click.group()
@click.pass_context
def scope(ctx):
    """Commands related to scopes for associating with roles"""
    ctx.context = ctx.parent.context


@scope.command('list', hidden=hide_admin_cmds())
@table_format_option()
def scope_list(out_format: str):
    """
    Get the list of scopes defined for a tenant
    """
    list_scopes(out_format)
