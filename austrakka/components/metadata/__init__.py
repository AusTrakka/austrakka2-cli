# pylint: disable=redefined-outer-name
from io import BufferedReader
import click

from .funcs import add_metadata_submission
from ..species.opts import species as species_opt


@click.group()
@click.pass_context
def metadata(ctx):
    """Commands related to metadata submissions"""
    ctx.creds = ctx.parent.creds


@metadata.command('add')
@click.argument('file', type=click.File('rb'))
@species_opt
def submission_add(file: BufferedReader, species: int):
    """Upload metadata submission to AusTrakka"""
    add_metadata_submission(file, species)
