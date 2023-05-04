# pylint: disable=redefined-outer-name
from io import BufferedReader
import click

from austrakka.utils.options import opt_proforma
from austrakka.utils.options import opt_is_append
from austrakka.utils.options import opt_group_name
from austrakka.components.metadata.funcs import add_metadata
from austrakka.components.metadata.funcs import validate_metadata
from austrakka.components.metadata.funcs import append_metadata
from austrakka.components.metadata.funcs import list_metadata
from austrakka.utils.output import table_format_option


@click.group()
@click.pass_context
def metadata(ctx):
    """Commands related to metadata submissions"""
    ctx.context = ctx.parent.context


@metadata.command('add')
@click.argument('file', type=click.File('rb'))
@opt_proforma()
def submission_add(file: BufferedReader, proforma: str):
    """Upload metadata submission to AusTrakka"""
    add_metadata(file, proforma)


@metadata.command('append')
@click.argument('file', type=click.File('rb'))
@opt_proforma()
def submission_append(file: BufferedReader, proforma: str):
    """
    Upload metadata to be appended to existing samples.
    The append operation does not require (or accept) Owner_group.
    The specified pro forma must contain Seq_ID and metadata fields
    to be updated. All samples must already exist in AusTrakka.
    """
    append_metadata(file, proforma)


@metadata.command('validate')
@click.argument('file', type=click.File('rb'))
@opt_proforma()
@opt_is_append()
def submission_validate(file: BufferedReader, proforma: str, is_append: bool):
    """Check uploaded content for errors and warnings. This is a read-only
    action. No data will modified."""
    validate_metadata(file, proforma, is_append)


@metadata.command('list')
@opt_group_name()
@table_format_option()
def metadata_list(group_name: str, out_format: str):
    """List metadata for a specific group"""
    list_metadata(group_name, out_format)
