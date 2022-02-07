# pylint: disable=redefined-outer-name
from io import BufferedReader
import click

from .funcs import add_sequence_submission


@click.group()
@click.pass_context
def seq(ctx):
    """Commands related to sequences"""
    ctx.creds = ctx.parent.creds


@seq.command('add')
@click.argument('file', type=click.File('rb'))
def submission_add(file: BufferedReader):
    """Upload sequence submission to AusTrakka"""
    add_sequence_submission(file)
