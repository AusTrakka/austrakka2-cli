# pylint: disable=redefined-outer-name
from io import BufferedReader
from typing import Tuple

import click

from .funcs import add_sequence_submission


@click.group()
@click.pass_context
def seq(ctx):
    """Commands related to sequences"""
    ctx.creds = ctx.parent.creds


@seq.command('add')
@click.argument('files', type=click.File('rb'), nargs=-1)
@click.option(
    "--csv",
    type=click.File('rb'),
    default=None,
    help="CSV with Sample to Sequence mapping"
)
def submission_add(files: Tuple[BufferedReader], csv: BufferedReader):
    """Upload sequence submission to AusTrakka

    FILES: list of fasta files
    """
    add_sequence_submission(files, csv)
