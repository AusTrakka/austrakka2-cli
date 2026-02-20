import click

from austrakka.components.log.funcs import list_logs
from austrakka.utils.cmd_filter import hide_admin_cmds
from austrakka.utils.options import opt_identifier, opt_record_type, opt_view_type
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
@click.option('--start', help='Start datetime to filter from', required=False)
@click.option('--end', help='End datetime to filter to', required=False)
@click.option('--submitter', help='Submitter global ID to filter on', required=False)
@click.option('--resource', help='Resource name to filter on', required=False)
@click.option('--resource-type', help='Resource type to filter on', required=False)
@table_format_option()
@opt_view_type()
def activity_list(
    record_type: str,
    global_id: str,
    out_format: str,
    view_type: str,
    start: str,
    end: str,
    submitter: str,
    resource: str,
    resource_type: str,
):
    list_logs(
        record_type,
        global_id,
        start,
        end,
        submitter,
        resource,
        resource_type,
        out_format,
        view_type,
    )
