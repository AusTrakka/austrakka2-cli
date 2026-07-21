import click

from trakka.utils.output import table_format_option
from trakka.utils.cmd_filter import hide_admin_cmds
from trakka.utils.options import *
from .funcs import \
    add_field, \
    remove_field, \
    list_field


@click.group()
@click.pass_context
def field(ctx):
    """Commands related to org fields"""
    ctx.context = ctx.parent.context


@field.command('add', hidden=hide_admin_cmds())
@opt_identifier(help="Org identifier")
@opt_field_name()
def group_add_field(identifier, field_names):
    '''
    Add fields to the data view for the given org
    '''
    add_field(identifier, field_names)


@field.command('remove', hidden=hide_admin_cmds())
@opt_identifier(help="Org identifier")
@opt_field_name()
def group_remove_field(identifier, field_names):
    '''
    Remove fields from the data view for the given org
    '''
    remove_field(identifier, field_names)


@field.command('list', hidden=hide_admin_cmds())
@opt_identifier(help="Org identifier")
@table_format_option()
@opt_view_type()
def group_list_field(identifier: str, out_format: str, view_type: str):
    '''
    List of fields in data view for the given org
    '''
    list_field(identifier, out_format, view_type)
