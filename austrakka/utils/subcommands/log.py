import click

from austrakka.utils.privilege import TENANT_RESOURCE
from austrakka.components.log.funcs import list_logs
from austrakka.utils.output import table_format_option
from austrakka.utils.options import opt_identifier, opt_view_type

def log_subcommands(root_type: str):
    root_type_name = 'system' if root_type == TENANT_RESOURCE else root_type.lower()
    
    @click.group(help=f"Commands related to {root_type_name} logs")
    @click.pass_context
    def log(ctx):
        ctx.context = ctx.parent.context

    @log.command('list')
    @( # This adds the identifier parameter only if the root_type is not tenant
        opt_identifier(
            required=True,
            help=f"Identifier of the {root_type_name} for which to retrieve logs")
        if root_type != TENANT_RESOURCE else lambda f: f
    )
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
        start: str,
        end: str,
        event_type: str,
        submitter: str,
        resource_identifier: str,
        resource_type: str,
        out_format: str,
        view_type: str,
        global_id: str = None,
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
