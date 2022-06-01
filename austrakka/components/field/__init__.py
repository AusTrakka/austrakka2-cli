import click
from typing import List

from austrakka.utils.output import table_format_option
from .funcs import list_fields, add_field, update_field
from ...utils.options import *


@click.group()
@click.pass_context
def field(ctx):
    """Commands related to metadata fields"""
    ctx.creds = ctx.parent.creds


@field.command('list')
@table_format_option()
def field_list(table_format: str):
    """List metadata fields understood by AusTrakka"""
    list_fields(table_format)


@field.command('add')
@opt_name(help_text="Field name")
@opt_fieldtype()
@click.option('--colour-nodes', 'colour_nodes', flag_value='viz',
              help="This field may be used to colour nodes on the tree")
@click.option('--no-colour-nodes', 'colour_nodes', flag_value='no_viz',
              help="This field may not be used to colour nodes on the tree")  # check if default is None
@click.option('-O', '--column-order', type=int, default=9000,
              help="Default order in which this column will be sorted in tables relative to other fields. If no value is specifed, the column will be placed after ordered columns.")
@click.option('--show/--no-show', default=True, type=bool,
              help="Whether the column will be shown in relevant tables on load, rather than needing to be selected in the column picker.")
def field_add(
        name: str,
        field_type: str,
        colour_nodes: str,
        column_order: int,
        show: bool):
    """Add a metadata field to AusTrakka"""
    add_field(name, field_type, colour_nodes, column_order, show)


@field.command('update')
@click.argument('fieldname')
@opt_name(required=False,
          help_text="New field name - if this argument is provided, the field name will be changed")
@opt_fieldtype(required=False)
@click.option('--colour-nodes', 'colour_nodes', flag_value='viz',
              help="This field may be used to colour nodes on the tree")
@click.option('--no-colour-nodes', 'colour_nodes', flag_value='no_viz',
              help="This field may not be used to colour nodes on the tree")  # check if default is None
@click.option('-O', '--column-order', type=int, default=None,
              help="Default order in which this column will be sorted in tables relative to other fields. If no value is specifed, the column will be placed after ordered columns.")
@click.option('--show', 'set_show', flag_value='show',
              help="Whether the column will be shown in relevant tables on load, rather than needing to be selected in the column picker.")
@click.option('--no-show', 'set_show', flag_value='no_show',
              help="Whether the column will be shown in relevant tables on load, rather than needing to be selected in the column picker.")
def field_add(
        fieldname: str,
        name: str,
        field_type: str,
        colour_nodes: str,
        column_order: int,
        set_show: str):
    """Update a metadata field within AusTrakka"""
    update_field(
        fieldname,
        name,
        field_type,
        colour_nodes,
        column_order,
        set_show)
