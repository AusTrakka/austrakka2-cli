from typing import List
import click

from austrakka.utils.output import table_format_option
from .funcs import list_fieldtypes, add_fieldtype
from ...utils.options import *


@click.group()
@click.pass_context
def fieldtype(ctx):
    """Commands related to metadata field types"""
    ctx.creds = ctx.parent.creds


@fieldtype.command('list')
@table_format_option()
def fieldtype_list(table_format: str):
    """List metadata field types, including different categorical fields"""
    list_fieldtypes(table_format)


@fieldtype.command('add')
@opt_name(help_text="Type name")
@opt_description
@click.option('-v',
              '--value',
              multiple=True,
              help='Allowed value for this categorical field. Multiple may be entered; at least one is required.',
              type=click.STRING)
def fieldtype_add(name: str, description: str, value: List[str]):
    """Add a new categorical field type and its valid values"""
    add_fieldtype(name, description, validValues=value)
