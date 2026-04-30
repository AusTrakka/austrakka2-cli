import click

from trakka.utils.options import opt_identifier, opt_view_type
from trakka.utils.output import object_format_option, table_format_option
from trakka.utils.option_utils import create_option
from trakka.components.admin.rawlog.funcs import \
    show_raw_log, list_raw_logs, regenerate_raw_log, regenerate_raw_log_bulk

def opt_spec_filter():
    return create_option(
        '--spec', help='Type class of raw event to filter on', required=False)

def opt_start_datetime_filter():
    return create_option(
        '--start', help='Start datetime to filter from', required=False)

def opt_end_datetime_filter():
    return create_option(
        '--end', help='End datetime to filter to', required=False)

def opt_submitter_filter():
    return create_option(
        '--submitter', help='Submitter global ID to filter on', required=False)

# pylint: disable=redefined-builtin
def opt_allow_no_filters(help="Allow listing without any filters, which will return ALL raw logs"):
    return create_option(
        '--allow-no-filters', is_flag=True, default=False, help=help)

@click.group('rlog')
@click.pass_context
def rawlog(ctx):
    """Commands related to raw logs"""
    ctx.context = ctx.parent.context

@rawlog.command('show')
@opt_identifier(help="Raw log global ID", var_name="global_id")
@object_format_option()
def rawlog_show(global_id: str, out_format: str):
    '''
    Get a single raw log by global ID.
    '''
    show_raw_log(global_id, out_format)

@rawlog.command('list')
@opt_spec_filter()
@opt_start_datetime_filter()
@opt_end_datetime_filter()
@opt_submitter_filter()
@opt_allow_no_filters()
@table_format_option(default='json')
@opt_view_type()
def rawlog_list(spec: str, start: str, end: str, submitter: str, allow_no_filters: bool,
                out_format: str, view_type: str):
    '''
    Get a list of raw logs entries.
    '''
    list_raw_logs(spec, start, end, submitter, allow_no_filters, out_format, view_type)

@rawlog.command('regen')
@opt_identifier(help="Raw log global ID", var_name="global_id")
def rawlog_regenerate(global_id: str):
    """Regenerate logs derived from a raw log entry"""
    regenerate_raw_log(global_id)

@rawlog.command('regen-bulk')
@opt_spec_filter()
@opt_start_datetime_filter()
@opt_end_datetime_filter()
@opt_submitter_filter()
@opt_allow_no_filters(help="Allow listing without any filters, which will regenerate ALL logs")
def rawlog_bulk_regen(spec: str, start: str, end: str, submitter: str, allow_no_filters: bool):
    '''
    Regenerate logs derived from multiple raw log entries.
    '''
    regenerate_raw_log_bulk(spec, start, end, submitter, allow_no_filters)
