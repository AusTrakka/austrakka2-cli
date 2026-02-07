import click

from austrakka.components.log.funcs import list_logs
from austrakka.utils.cmd_filter import hide_admin_cmds
from austrakka.utils.options import opt_identifier, opt_record_type, opt_view_type, opt_timezone
from austrakka.utils.output import table_format_option
from austrakka.utils.privilege import TENANT_RESOURCE

GLOBAL_ID_HELP="ID; either a global ID or abbreviation. Required for non-tenant"

@click.group()
@click.pass_context
def log(ctx):
    """Commands related to logs"""
    ctx.context = ctx.parent.context

# pylint: disable=duplicate-code
@log.command('list', hidden=hide_admin_cmds())
@opt_record_type(default=TENANT_RESOURCE)
@opt_identifier(
    required=False,
    default=None,
    help=GLOBAL_ID_HELP,
)
@table_format_option()
@opt_view_type()
@opt_timezone()
def activity_list(record_type: str, global_id: str, out_format: str, view_type: str, timezone: str):
    list_logs(record_type, global_id, out_format, view_type, timezone)
    
