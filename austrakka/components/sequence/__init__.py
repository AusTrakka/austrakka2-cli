# pylint: disable=redefined-outer-name
from io import BufferedReader
from typing import Tuple

import click

from austrakka.utils.options import opt_csv
from austrakka.utils.options import opt_seq_type
from austrakka.utils.enums.seq import FASTA_UPLOAD_TYPE
from .funcs import add_fasta_submission
from .funcs import add_fastq_submission
from .funcs import download_fastq


@click.group()
@click.pass_context
def seq(ctx):
    """Commands related to sequences"""
    ctx.creds = ctx.parent.creds


@seq.command('add')
@click.argument('files', type=click.File('rb'), nargs=-1)
@opt_csv(help_text='CSV with Sample to Sequence mapping')
@opt_seq_type
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


@seq.command('download')
@click.argument('sample_name')
@opt_seq_type
def download(
        sample_name: str,
        seq_type: str,
):
    """Upload sequence submission to AusTrakka

    FILES: list of fasta files
    """
    # pylint: disable=expression-not-assigned
    
    
    download_fastq(sample_name)
