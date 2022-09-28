# pylint: disable=redefined-outer-name
from io import BufferedReader

import os
import click

from austrakka.utils.options import opt_csv
from austrakka.utils.options import opt_seq_type
from austrakka.utils.options import opt_output_dir
from austrakka.utils.options import opt_species
from austrakka.utils.options import opt_read
from austrakka.utils.enums.seq import FASTA_UPLOAD_TYPE
from austrakka.utils.enums.seq import FASTQ_UPLOAD_TYPE
from austrakka.utils.fs import create_dir
from .funcs import add_fasta_submission
from .funcs import add_fastq_submission
from .funcs import fetch_samples_names_by_species
from .funcs import fetch_seq_download_info
from .funcs import take_sample_names
from .funcs import throw_if_empty
from .funcs import download_fasta_for_each_sample
from .funcs import download_fastq_for_each_sample


@click.group()
@click.pass_context
def seq(ctx):
    """Commands related to sequences"""
    ctx.creds = ctx.parent.creds


@seq.command('add')
@opt_csv(help_text='CSV with Sample to Sequence mapping', required=True)
@opt_seq_type
def submission_add(
        csv_file: BufferedReader,
        seq_type: str
):
    """
    Upload sequence submission to AusTrakka

    The following CSV mapping fields are required:\n
        For FASTA:\n
            SampleId: The sample name in AusTrakka\n
            FileName: The local path of the fasta file to be uploaded\n
            FastaId: The sequence id in the fasta file\n

        For FASTQ:\n
            Seq_ID: The sample name in AusTrakka\n
            filepath1: The local path of the first read to be uploaded\n
            filepath2: The local path of the second read to be uploaded
    """
    # pylint: disable=expression-not-assigned
    add_fasta_submission(csv_file) \
        if seq_type == FASTA_UPLOAD_TYPE \
        else add_fastq_submission(csv_file)


@seq.command('get')
@opt_output_dir
@opt_species()
@opt_seq_type
@opt_read
def get(
        output_dir,
        species: str,
        seq_type: str,
        read: str,
):
    """Download sequence files to the local drive

    EXAMPLE 1: Download Fastq with both Reads for species SARS-CoV-2

        austrakka seq get -t fastq --species SARS-CoV-2 --outdir ~/Downloads/fastq-files


    EXAMPLE 2: Download Fasta species SARS-CoV-2

        austrakka seq get -t fasta --species SARS-CoV-2 --outdir ~/Downloads/fasta-files


    """
    # pylint: disable=expression-not-assigned
    if not os.path.exists(output_dir):
        create_dir(output_dir)

    data = fetch_samples_names_by_species(species)

    if seq_type == FASTQ_UPLOAD_TYPE:
        samples_names = take_sample_names(data, 'hasFastq')
    else:
        samples_names = take_sample_names(data, 'hasFasta')

    throw_if_empty(samples_names, f'No samples found for species: {species}')
    samples_seq_info = fetch_seq_download_info(samples_names)

    if seq_type == FASTQ_UPLOAD_TYPE:
        download_fastq_for_each_sample(output_dir, samples_seq_info, read)
    else:
        download_fasta_for_each_sample(output_dir, samples_seq_info)
