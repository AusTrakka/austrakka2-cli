import click

from trakka.components.log.funcs import list_logs
from trakka.utils.output import table_format_option
from trakka.utils.options import opt_identifier, opt_view_type


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
            'Start datetime to filter from '
            '(e.g. "12pm", "3 days ago", "2026-03-03T15:00", "2026-03-03T15:00:00+12:00")'
        ),
        required=False
    )
    @click.option(
        '--end',
        help=(
            'End datetime to filter to '
            '(e.g. "12pm", "3 days ago", "2026-03-03T15:00", "2026-03-03T15:00:00+12:00")'
        ),
        required=False
    )
    @click.option('--event-type', help='Event type to filter on', required=False)
    @click.option('--submitter', help='Submitter display name to filter on', required=False)
    @click.option(
        '--resource-identifier',
        help='Resource name or identifier to filter on (strict match only)',
        required=False
    )
    @click.option('--resource-type', help='Resource type to filter on', required=False)
    @table_format_option()
    @opt_view_type()
    def activity_get(
        global_id: str,
        start: str,
        end: str,
        event_type: str,
        submitter: str,
        resource_identifier: str,
        resource_type: str,
        out_format: str,
        view_type: str
    ):
        list_logs(
            root_type,
            global_id,
            start,
            end,
            event_type,
            submitter,
            resource_identifier,
            resource_type,
            out_format,
            view_type
        )

    return log
