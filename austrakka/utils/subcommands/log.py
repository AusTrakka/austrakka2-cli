import click

from austrakka.components.log.funcs import list_logs
from austrakka.utils.output import table_format_option
from austrakka.utils.options import opt_identifier, opt_view_type, opt_timezone


def log_subcommands(root_type: str):
    @click.group(help=f"Commands related to {root_type.lower()} logs")
    @click.pass_context
    def log(ctx):
        ctx.context = ctx.parent.context

    @log.command('list')
    @opt_identifier()
    @table_format_option()
    @opt_view_type()
    @opt_timezone()
    def activity_get(global_id: str, out_format: str, view_type: str, timezone: str):
        list_logs(root_type, global_id, out_format, view_type, timezone)

    return log
