# pylint: disable=redefined-outer-name
from io import BufferedReader
import click

from austrakka.utils.options import opt_proforma
from .funcs import add_metadata


@click.group()
@click.pass_context
def metadata(ctx):
    """Commands related to metadata submissions"""
    ctx.creds = ctx.parent.creds


@metadata.command('add')
@click.argument('file', type=click.File('rb'))
@opt_proforma
def submission_add(file: BufferedReader, proforma: str):
    """Upload metadata submission to AusTrakka"""
    add_metadata(file, proforma)
