from typing import List

import click

from austrakka.utils.options import opt_field_name, opt_identifier
from austrakka.utils.output import table_format_option
from austrakka.utils.output import FORMATS

from .funcs import list_metadata
from .funcs import list_metadata_by_field

@click.group()
@click.pass_context
def metadata(ctx):
    """Commands to query for metadata in an org
    """
    ctx.context = ctx.parent.context


@metadata.command('list')
@opt_identifier(help="Org identifier")
@opt_field_name(
    required=False, 
    help="Fields to retrieve; if none specified, all fields will be retrieved")
@table_format_option(FORMATS.CSV)
def metadata_list(identifier: str, field_names: List[str], out_format: str):
    """List metadata for an org"""
    if len(field_names)==0:
        list_metadata(identifier, out_format)
    else:
        list_metadata_by_field(identifier, field_names, out_format)
