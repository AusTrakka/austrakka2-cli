from typing import List

import click

from austrakka.utils.cmd_filter import hide_admin_cmds
from austrakka.utils.output import table_format_option
from austrakka.components.fieldtype.funcs import list_fieldtypes
from austrakka.components.fieldtype.funcs import add_fieldtype
from austrakka.components.fieldtype.funcs import update_fieldtype
from austrakka.components.fieldtype.value import value
from austrakka.utils.options import opt_description
from austrakka.utils.options import opt_name
from austrakka.utils.options import opt_fieldtype_value
from austrakka.utils.options import opt_is_active
from austrakka.utils.cmd_filter import show_admin_cmds


@click.group()
@click.pass_context
def fieldtype(ctx):
    """Commands related to metadata field types"""
    ctx.context = ctx.parent.context


# pylint: disable=expression-not-assigned
fieldtype.add_command(value) if show_admin_cmds() else None


@fieldtype.command('list')
@table_format_option()
def fieldtype_list(out_format: str):
    """List metadata field types, including different categorical fields"""
    list_fieldtypes(out_format)


@fieldtype.command('add', hidden=hide_admin_cmds())
@opt_name(help="Type name")
@opt_description()
@opt_fieldtype_value()
def fieldtype_add(name: str, description: str, values: List[str]):
    """Add a new categorical field type and its valid values"""
    add_fieldtype(name, description, valid_values=values)


@fieldtype.command('update', hidden=hide_admin_cmds())
@click.argument('name', type=str)
@opt_description(required=False)
@opt_is_active(is_update=True)
def fieldtype_update(
        name: str,
        description: str,
        is_active: bool,
):
    """Update a fieldtype"""
    update_fieldtype(name, description, is_active)
