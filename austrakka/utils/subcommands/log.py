import click

from austrakka.components.log.funcs import list_logs
from austrakka.utils.output import table_format_option
from austrakka.utils.options import opt_identifier, opt_view_type


def log_subcommands(root_type: str):
    @click.group(help=f"Commands related to {root_type.lower()} logs")
    @click.pass_context
    def log(ctx):
        ctx.context = ctx.parent.context

    @log.command('list')
    @opt_identifier()
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
    @click.option('--submitter', help='Submitter display name to filter on', required=False)
    @click.option('--resource', help='Resource name to filter on', required=False)
    @click.option('--resource-type', help='Resource type to filter on', required=False)
    @table_format_option()
    @opt_view_type()
    def activity_get(
        global_id: str,
        start: str,
        end: str,
        submitter: str,
        resource: str,
        resource_type: str,
        out_format: str,
        view_type: str
    ):
        list_logs(
            root_type,
            global_id,
            start,
            end,
            submitter,
            resource,
            resource_type,
            out_format,
            view_type
        )

    return log
