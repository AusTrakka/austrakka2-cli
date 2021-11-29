# pylint: disable=redefined-outer-name
from io import BufferedReader
import click

from .funcs import add_submission
from ..species.opts import species


@click.group()
@click.pass_context
def submission(ctx):
    '''Commands related to submissions'''
    ctx.creds = ctx.parent.creds


@submission.command('add')
@click.argument('file', type=click.File('rb'))
@species
def submission_add(file: BufferedReader, species: int):
    '''Upload submission to AusTrakka'''
    add_submission(file, species)
