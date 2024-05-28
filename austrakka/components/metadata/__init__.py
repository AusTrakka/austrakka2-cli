
from typing import List

# pylint: disable=redefined-outer-name
from io import BufferedReader
import click

from austrakka.utils.options import opt_proforma, opt_batch_size
from austrakka.utils.options import opt_is_update
from austrakka.utils.options import opt_group_name
from austrakka.utils.options import opt_blanks_delete
from austrakka.utils.options import opt_field_name
from austrakka.components.metadata.funcs import add_metadata
from austrakka.components.metadata.funcs import validate_metadata
from austrakka.components.metadata.funcs import append_metadata
from austrakka.components.metadata.funcs import list_metadata, list_metadata_by_field
from austrakka.utils.output import table_format_option, FORMATS

ADD_APPEND_BATCH_SIZE_HELP = (
    'The number of rows to split the metadata upload into before uploading. '
    'If the file size is below this value, the file will not be split. '
    'An upload record will be recorded in the database per batch, and '
    'validation and success messages will be returned per batch. '
    'Only CSV files will be batched; Excel files will be uploaded as one file. '
    'A negative or 0 value can be used to indicate no batching.'
)


@click.group()
@click.pass_context
def metadata(ctx):
    """Commands related to metadata submissions"""
    ctx.context = ctx.parent.context
    

@metadata.command('add')
@click.argument('file', type=click.File('rb'))
@opt_proforma()
@opt_blanks_delete()
@opt_batch_size(help=ADD_APPEND_BATCH_SIZE_HELP,
                default=5000)
def submission_add(
        file: BufferedReader,
        proforma: str,
        blanks_will_delete: bool,
        batch_size: int):
    """Upload metadata submission to AusTrakka"""
    add_metadata(file, proforma, blanks_will_delete, batch_size)


@metadata.command('update')
@click.argument('file', type=click.File('rb'))
@opt_proforma()
@opt_blanks_delete()
@opt_batch_size(help=ADD_APPEND_BATCH_SIZE_HELP,
                default=5000)
def submission_append(
        file: BufferedReader, 
        proforma: str, 
        blanks_will_delete: bool,
        batch_size: int):   
    """
    Upload metadata to existing samples.
    The update operation does not require (or accept) Owner_group.
    The specified pro forma must contain Seq_ID and metadata fields
    to be updated. All samples must already exist in AusTrakka.
    """
    append_metadata(file, proforma, blanks_will_delete, batch_size)


@metadata.command('validate')
@click.argument('file', type=click.File('rb'))
@opt_proforma()
@opt_is_update()
@opt_batch_size(help='The number of rows to split the metadata upload into before uploading. '
                     'If the file size is below this value, the file will not be split. '
                     'Validation messages will be returned per batch.'
                     'A negative or 0 value can be used to indicate no batching.',
                default=5000)
def submission_validate(file: BufferedReader, proforma: str, is_update: bool, batch_size: int):
    """Check uploaded content for errors and warnings. This is a read-only
    action. No data will modified."""
    validate_metadata(file, proforma, is_update, batch_size)


@metadata.command('list')
@opt_group_name()
@opt_field_name(
    required=False, 
    help="Fields to retrieve; if none specified, all fields will be retrieved")
@table_format_option(FORMATS.CSV)
def metadata_list(group_name: str, field_names: List[str], out_format: str):
    """List metadata for a specific group"""
    if len(field_names)==0:
        list_metadata(group_name, out_format)
    else:
        list_metadata_by_field(group_name, field_names, out_format)
