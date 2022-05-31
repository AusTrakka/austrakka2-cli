import click
from typing import List

from austrakka.utils.output import table_format_option
from .funcs import list_fieldtypes
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
