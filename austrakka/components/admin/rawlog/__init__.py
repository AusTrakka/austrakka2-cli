import click

from austrakka.utils.options import opt_global_id, opt_view_type, opt_timezone
from austrakka.utils.output import object_format_option, table_format_option
from austrakka.components.admin.rawlog.funcs import show_raw_log, list_raw_logs

@click.group('rlog')
@click.pass_context
def rawlog(ctx):
    """Commands related to raw logs"""
    ctx.context = ctx.parent.context

@rawlog.command('show')
@opt_global_id(help="Raw log global ID")
@object_format_option()
@opt_timezone()
def rawlog_show(global_id: str, out_format: str, opt_timezone: str):
    '''
    Get a single raw log by global ID.
    '''
    show_raw_log(global_id, out_format, timezone)

@rawlog.command('list')
@click.option('--spec', help='Type class of raw event to filter on', required=False)
@click.option('--start', help='Start datetime to filter from (ISO 8601)', required=False)
@click.option('--end', help='End datetime to filter to (ISO 8601)', required=False)
@click.option('--submitter', help='Submitter global ID to filter on', required=False)
@click.option('--allow-no-filters', is_flag=True, default=False,
              help="Allow listing without any filters, which will return ALL raw logs")
@table_format_option(default='json')
@opt_view_type()
@opt_timezone()
def rawlog_list(spec: str, start: str, end: str, submitter: str, allow_no_filters: bool,
                out_format: str, view_type: str, timezone: str):
    '''
    Get a list of raw logs entries.
    '''
    list_raw_logs(spec, start, end, submitter, allow_no_filters, out_format, view_type, timezone)
