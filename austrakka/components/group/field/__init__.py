from typing import List
import click

from austrakka.utils.output import table_format_option
from austrakka.utils.cmd_filter import hide_admin_cmds
from austrakka.utils.options import *
from .funcs import \
    add_field_group, \
    remove_field_group, \
    list_field_group


@click.group()
@click.pass_context
def field(ctx):
    """Commands related to group fields access"""
    ctx.context = ctx.parent.context


@field.command('add', hidden=hide_admin_cmds())
@click.argument('name', type=str)
@opt_field_name()
def group_add_field(name, field_names):
    '''
    Allow fields to show for the given group.
    '''
    add_field_group(name, field_names)


@field.command('remove', hidden=hide_admin_cmds())
@click.argument('name', type=str)
@opt_field_name()
def group_remove_field(name, field_names):
    '''
    Deny fields from showing for the given group.
    '''
    remove_field_group(name, field_names)


@field.command('list', hidden=hide_admin_cmds())
@click.argument('name', type=str)
@table_format_option()
def group_list_field(name: str, out_format: str):
    '''
    List of fields allowed to show for the given group.
    '''
    list_field_group(name, out_format)
