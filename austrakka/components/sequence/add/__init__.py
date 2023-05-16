
from io import BufferedReader

import click

from austrakka.utils.options import opt_csv
from ..funcs import add_fasta_submission
from ..funcs import add_fastq_submission


@click.group()
@click.pass_context
def add(ctx):
    """Commands to upload sequences"""
    ctx.context = ctx.parent.context


@add.command('fastq')
@opt_csv(help='CSV with mapping from Seq_ID to sequence files', required=True)
def seq_add_fastq(
        csv_file: BufferedReader
):
    """
    Upload FASTQ submission to AusTrakka

    The following CSV mapping fields are required:\n
            Seq_ID: The sample name in AusTrakka\n
            filepath1: The local path of the first read to be uploaded\n
            filepath2: The local path of the second read to be uploaded
    """
    add_fastq_submission(csv_file)


@add.command('fasta')
@click.argument('fasta_file', type=click.File('rb'))
def seq_add_fasta(
        fasta_file: BufferedReader
):
    """
    Upload FASTA submission to AusTrakka

    A single FASTA file should be supplied.
    Contig names must correspond to known Seq_IDs.

    If no record exists for these Seq_IDs you can first add them with the
    `austrakka metadata add` command, and may use the minimal proforma if
    you wish to specify no metadata other than sample ownership.
    """
    add_fasta_submission(fasta_file)
