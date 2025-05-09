import click

from austrakka.components.activity.funcs import get_activity_by_record_type
from austrakka.utils.output import table_format_option


def activity_subcommands(root_type: str):
    """
    Generate activity subcommands for a given root type.
    """
    @click.group(help=f"Commands related to {root_type.lower()} activity log")
    @click.pass_context
    def activity(ctx):
        ctx.context = ctx.parent.context

    @activity.command('get')
    @click.argument('record-global-id', type=str)
    @table_format_option()
    def activity_get(record_global_id: str, out_format: str):
        get_activity_by_record_type(root_type, record_global_id, out_format)

    return activity
