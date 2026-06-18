from typing import List

import click

from austrakka.utils.options import opt_field_name, opt_identifier
from austrakka.utils.output import table_format_option
from austrakka.utils.output import FORMATS

from .funcs import get_metadata
from .funcs import get_metadata_by_field

# pylint: disable=R0801
@click.group()
@click.pass_context
def metadata(ctx):
    """Commands to query for metadata in an org
    """
    ctx.context = ctx.parent.context


@metadata.command('get')
@opt_identifier(help="Org identifier")
@opt_field_name(
    required=False, 
    help="Fields to retrieve; if none specified, all fields will be retrieved")
@table_format_option(FORMATS.CSV)
def metadata_get(identifier: str, field_names: List[str], out_format: str):
    """List metadata for an org"""
    if len(field_names)==0:
        get_metadata(identifier, out_format)
    else:
        get_metadata_by_field(identifier, field_names, out_format)
