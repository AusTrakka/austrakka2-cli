# pylint: disable=redefined-outer-name
from io import BufferedReader
from typing import Tuple

import click

from austrakka.utils.options import csv
from .funcs import add_fasta_submission
from .funcs import add_fastq_submission

FASTQ_UPLOAD_TYPE = 'fastq'
FASTA_UPLOAD_TYPE = 'fasta'


@click.group()
@click.pass_context
def seq(ctx):
    """Commands related to sequences"""
    ctx.creds = ctx.parent.creds


@seq.command('add')
@click.argument('files', type=click.File('rb'), nargs=-1)
@csv(help_text='CSV with Sample to Sequence mapping')
@click.option(
    '--type',
    'seq_type',
    required=True,
    type=click.Choice([FASTA_UPLOAD_TYPE, FASTQ_UPLOAD_TYPE]),
    help='Sequence format',
)
def submission_add(
        files: Tuple[BufferedReader],
        csv_file: BufferedReader,
        seq_type: str
):
    """Upload sequence submission to AusTrakka

    FILES: list of fasta files
    """
    # pylint: disable=expression-not-assigned
    add_fasta_submission(files, csv_file) \
        if seq_type == FASTA_UPLOAD_TYPE \
        else add_fastq_submission(files, csv_file)
