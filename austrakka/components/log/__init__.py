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
@click.option(
    '--start',
    help=(
        'Start datetime to filter from, e.g., 2026-01-01T00:00:00. '
        'If no timezone is provided, the default timezone will be used.'
    ),
    required=False
)
@click.option(
    '--end',
    help=(
        'End datetime to filter to, e.g., 2026-01-01T23:59:59. '
        'If no timezone is provided, the default timezone will be used.'
    ),
    required=False
)
@click.option('--event-type', help='Event type to filter on', required=False)
@click.option('--submitter', help='Submitter display name to filter on', required=False)
@click.option('--resource-identifier', help='Resource name or identifier to filter on (strict match only)', required=False)
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
    event_type: str,
    submitter: str,
    resource_identifier: str,
    resource_type: str,
):
    list_logs(
        record_type,
        global_id,
        start,
        end,
        event_type,
        submitter,
        resource_identifier,
        resource_type,
        out_format,
        view_type,
    )
