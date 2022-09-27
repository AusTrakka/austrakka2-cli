from typing import List

import click

from austrakka.utils.cmd_filter import hide_admin_cmds
from austrakka.utils.output import table_format_option
from austrakka.components.fieldtype.funcs import list_fieldtypes, add_fieldtype
from austrakka.components.fieldtype.value import value
from austrakka.utils.options import opt_description
from austrakka.utils.options import opt_name
from austrakka.utils.options import opt_fieldtype_value
from austrakka.utils.cmd_filter import show_admin_cmds


@click.group()
@click.pass_context
def fieldtype(ctx):
    """Commands related to metadata field types"""
    ctx.creds = ctx.parent.creds


# pylint: disable=expression-not-assigned
fieldtype.add_command(value) if show_admin_cmds() else None


@fieldtype.command('list')
@table_format_option()
def fieldtype_list(table_format: str):
    """List metadata field types, including different categorical fields"""
    list_fieldtypes(table_format)


@fieldtype.command('add', hidden=hide_admin_cmds())
@opt_name(help_text="Type name")
@opt_description()
@opt_fieldtype_value()
def fieldtype_add(name: str, description: str, values: List[str]):
    """Add a new categorical field type and its valid values"""
    add_fieldtype(name, description, valid_values=values)
