import click

from austrakka.utils.output import table_format_option
from austrakka.utils.cmd_filter import hide_admin_cmds
from .funcs import list_fields, add_field, update_field, disable_field, enable_field, \
    list_field_groups, list_field_projects, list_field_proformas
from ...utils.options import *


@click.group()
@click.pass_context
def field(ctx):
    """Commands related to metadata fields"""
    ctx.context = ctx.parent.context


@field.command('list')
@opt_view_type()
@table_format_option()
def field_list(view_type: str, out_format: str):
    """List metadata fields understood by AusTrakka"""
    list_fields(view_type, out_format)


@field.command('add', hidden=hide_admin_cmds())
@opt_name(help="Field name")
@opt_fieldtype()
@opt_description(
    required=False,
    default="",
    help="This field describes the purpose of the metadata field. "
         "Its value is also used for generating XLSX pro forma files.")
@create_option('--nndss', 'nndss',
               help="The corresponding National Notifiable Diseases Surveillance System label, "
                    "where it exists.")
@create_option('-O', '--column-order', type=int, default=9000,
               help="Default order in which this column will be sorted in tables relative to other "
                    "fields. If no value is specifed, the column will be placed after ordered "
                    "columns.")
@click.option('--viz/--no-viz', default=False,
              help="This field may be used for colour visualisation in trees or plots")
@opt_private()
def field_add(
        name: str,
        description: str,
        nndss: str,
        field_type: str,
        viz: bool,
        column_order: int,
        is_private: bool,
):
    """Add a metadata field to AusTrakka"""
    add_field(name, description, nndss, field_type, viz, column_order, is_private)


@field.command('update', hidden=hide_admin_cmds())
@click.argument('fieldname')
@opt_name(required=False,
          help="New field name - if this argument is provided, the field name will be changed")
@opt_fieldtype(required=False)
@opt_description(required=False, help="This field describes the purpose of the metadata field. "
                                      "Its value is also used for generating XLSX pro forma files.")
@create_option('--nndss', 'nndss',
               help="The corresponding National Notifiable Diseases Surveillance System label, "
                    "where it exists.")
@create_option('-O', '--column-order', type=int, default=None,
               help="Default order in which this column will be sorted in tables relative to other "
                    "fields. If no value is specifed, the column will be placed after ordered "
                    "columns.")
@opt_private(is_update=True)
@click.option('--viz/--no-viz', default=None,
              help="This field may be used for colour visualisation in trees or plots")
def field_update(
        fieldname: str,
        name: str,
        description: str,
        nndss: str,
        field_type: str,
        viz: bool,
        column_order: int,
        is_private: bool,
):
    """Update a metadata field within AusTrakka"""
    update_field(
        fieldname,
        name,
        description,
        nndss,
        field_type,
        viz,
        column_order,
        is_private
    )


@field.command('list-groups', hidden=hide_admin_cmds())
@click.argument('fieldname')
@table_format_option()
def field_list_groups(fieldname: str, out_format: str):
    """List groups that a metadata field belongs to"""
    list_field_groups(fieldname, out_format)


@field.command('list-projects', hidden=hide_admin_cmds())
@click.argument('fieldname')
@table_format_option()
def field_list_projects(fieldname: str, out_format: str):
    """List projects that a metadata field belongs to"""
    list_field_projects(fieldname, out_format)


@field.command('list-proformas', hidden=hide_admin_cmds())
@click.argument('fieldname')
@table_format_option()
def field_list_proformas(fieldname: str, out_format: str):
    """List proformas that a metadata field belongs to"""
    list_field_proformas(fieldname, out_format)


@field.command('disable', hidden=hide_admin_cmds())
@click.argument('fieldname')
def field_disable(fieldname: str):
    """Disable a metadata field within AusTrakka"""
    disable_field(fieldname)


@field.command('enable', hidden=hide_admin_cmds())
@click.argument('fieldname')
def field_enable(fieldname: str):
    """Enable a metadata field within AusTrakka"""
    enable_field(fieldname)
