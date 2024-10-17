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
@opt_view_type()
@table_format_option()
def scope_list(view_type: str, out_format: str):
    """
    Get the list of scopes defined for a tenant
    """
    list_scopes(view_type, out_format)
