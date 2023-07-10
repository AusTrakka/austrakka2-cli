from austrakka.utils.output import table_format_option
from austrakka.utils.cmd_filter import hide_admin_cmds
from ...utils.options import *
from .funcs import add_widget, list_widgets, update_widget, get_widget


@click.group()
@click.pass_context
def widget(ctx):
    """Commands related to dashboard widgets"""
    ctx.context = ctx.parent.context


@widget.command('list', hidden=hide_admin_cmds())
@table_format_option()
def widget_list(out_format: str):
    """List widgets available for use on dashboards"""
    list_widgets(out_format)


@widget.command('add', hidden=hide_admin_cmds())
@opt_name(help="Widget name. Must be unique.")
def widget_add(name: str,):
    """Add a widget for later inclusion on a dashboard in AusTrakka"""
    add_widget(name)


@widget.command('update', hidden=hide_admin_cmds())
@click.argument('widget-id', type=int)
@opt_new_name(help="New name to be assigned to the specified widget.")
def widget_update(widget_id: int, new_name: str):
    """Update an existing widget"""
    update_widget(widget_id, new_name)


@widget.command('get', hidden=hide_admin_cmds())
@click.argument('widget-id', type=int)
@table_format_option()
def widget_get(widget_id: int, out_format: str):
    """Get details of an existing widget"""
    get_widget(widget_id, out_format)
