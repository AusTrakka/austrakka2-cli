from typing import List
import click

from trakka.components.proforma.field.funcs import add_field_values
from trakka.components.proforma.field.funcs import list_fields
from trakka.components.proforma.field.funcs import remove_field_values
from trakka.components.proforma.field.funcs import update_field
from trakka.utils.output import table_format_option
from trakka.utils.options import *


@click.group()
@click.pass_context
def field(ctx):
    """Commands related to proformas fields"""
    ctx.context = ctx.parent.context


@field.command('update')
@opt_identifier(help="Identifier for a proforma")
@opt_identifier(
    help="Identifier for a field in the proforma", 
    option_name="--field-id",
    var_name="field_identifier",
    multiple=False,
)
@create_option(
    '--class',
    "metadata_class",
    type=click.Choice(["Enhanced", "Required", "Minimum"]),
    required=True,
    help='Metadata class',
)
@create_option(
    '--clear-values/--keep-values',
    "clear_values",
    type=bool,
    default=False,
    help='Clear all proforma restricted values',
)
def field_update(
    identifier: str, 
    field_identifier: str,
    metadata_class: str,
    clear_values: bool,
):
    """
    Updates a field in a proforma.
    """
    update_field(
        identifier, 
        field_identifier, 
        metadata_class, 
        clear_values
    )


@field.command('add-value')
@opt_identifier(help="Identifier for a proforma")
@opt_identifier(
    help="Identifier for a field in the proforma", 
    option_name="--field-id",
    var_name="field_identifier",
    multiple=False,
)
@opt_fieldtype_value()
def field_add_value(
    identifier: str, 
    field_identifier: str,
    values: List[str],
):
    """ Add a restricted value for a proforma field """
    add_field_values(identifier, field_identifier, values)


@field.command('remove-value')
@opt_identifier(help="Identifier for a proforma")
@opt_identifier(
    help="Identifier for a field in the proforma", 
    option_name="--field-id",
    var_name="field_identifier",
    multiple=False,
)
@opt_fieldtype_value()
def field_remove_value(
    identifier: str, 
    field_identifier: str,
    values: List[str],
):
    """ Remove a restricted value for a proforma field """
    remove_field_values(identifier, field_identifier, values)


@field.command('list')
@opt_identifier(help="Identifier for a proforma")
@table_format_option()
def field_list(identifier: str, out_format: str):
    """
    List proforma fields
    """
    list_fields(identifier, out_format)
