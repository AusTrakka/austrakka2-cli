import click

from austrakka.utils.output import table_format_option
from austrakka.utils.cmd_filter import hide_admin_cmds
from .funcs import list_fields, add_field, update_field
from ...utils.options import *


@click.group()
@click.pass_context
def field(ctx):
    """Commands related to metadata fields"""
    ctx.context = ctx.parent.context


@field.command('list')
@table_format_option()
def field_list(out_format: str):
    """List metadata fields understood by AusTrakka"""
    list_fields(out_format)


@field.command('add', hidden=hide_admin_cmds())
@opt_name(help="Field name")
@opt_fieldtype()
@click.option('-d', '--description', 'description',
              help="This field describes the purpose of the metadata field. "
                   "Its value is also used for generating XLSX pro forma files.")
@click.option('--nndss', 'nndss',
              help="The corresponding National Notifiable Diseases Surveillance System label, "
                   "where it exists.")
@click.option('--colour-nodes', 'colour_nodes', flag_value='viz',
              help="This field may be used to colour nodes on the tree")
@click.option('--no-colour-nodes', 'colour_nodes', flag_value='no_viz',
              help="This field may not be used to colour nodes on the tree")
@click.option('-O', '--column-order', type=int, default=9000,
              help="Default order in which this column will be sorted in tables relative to other '"
                   "fields. If no value is specifed, the column will be placed after ordered "
                    "columns.")
def field_add(
        name: str,
        description: str,
        nndss: str,
        field_type: str,
        colour_nodes: str,
        column_order: int,
):
    """Add a metadata field to AusTrakka"""
    add_field(name, description, nndss, field_type, colour_nodes, column_order)


@field.command('update', hidden=hide_admin_cmds())
@click.argument('fieldname')
@opt_name(required=False,
          help="New field name - if this argument is provided, the field name will be changed")
@opt_fieldtype(required=False)
@click.option('-d', '--description', 'description',
              help="This field describes the purpose of the metadata field. "
                   "Its value is also used for generating XLSX pro forma files.")
@click.option('--nndss', 'nndss',
              help="The corresponding National Notifiable Diseases Surveillance System label, " 
                   "where it exists.")
@click.option('--colour-nodes', 'colour_nodes', flag_value='viz',
              help="This field may be used to colour nodes on the tree")
@click.option('--no-colour-nodes', 'colour_nodes', flag_value='no_viz',
              help="This field may not be used to colour nodes on the tree")
@click.option('-O', '--column-order', type=int, default=None,
              help="Default order in which this column will be sorted in tables relative to other "
                   "fields. If no value is specifed, the column will be placed after ordered "
                   "columns.")
def field_update(
        fieldname: str,
        name: str,
        description: str,
        nndss: str,
        field_type: str,
        colour_nodes: str,
        column_order: int,
):
    """Update a metadata field within AusTrakka"""
    update_field(
        fieldname,
        name,
        description,
        nndss,
        field_type,
        colour_nodes,
        column_order,
    )
