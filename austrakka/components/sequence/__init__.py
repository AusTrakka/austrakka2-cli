# pylint: disable=redefined-outer-name
from io import BufferedReader
from typing import Tuple

import click

from austrakka.utils.api import RESPONSE_TYPE_ERROR
from austrakka.utils.output import create_response_object
from austrakka.utils.options import opt_csv
from austrakka.utils.options import opt_seq_type
from austrakka.utils.options import opt_species
from austrakka.utils.options import opt_read
from austrakka.utils.enums.seq import FASTA_UPLOAD_TYPE
from austrakka.utils.enums.seq import FASTQ_UPLOAD_TYPE
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
@click.argument('output_dir', type=click.Path(exists=False))
@opt_species
@opt_seq_type
@opt_read
def download(
        output_dir,
        species: int,
        seq_type: str,
        read: str,
):
    """Download sequence files to the local drive

    OUTPUT_DIR: The directory to save downloaded files. Saved files will
                be nested under a directory named after the sample.
    """
    # pylint: disable=expression-not-assigned
    if seq_type == FASTQ_UPLOAD_TYPE:
        download_fastq(str(species), output_dir, read)
    else:
        raise Exception(create_response_object(
            f"Downloading of {seq_type} not supported.",
            RESPONSE_TYPE_ERROR)
        )
