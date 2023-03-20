# pylint: disable=redefined-outer-name
from io import BufferedReader

import click

from austrakka.utils.output import table_format_option
from austrakka.utils.options import opt_csv
from austrakka.utils.options import opt_seq_type
from austrakka.utils.options import opt_output_dir
from austrakka.utils.options import opt_read
from austrakka.utils.options import opt_group
from austrakka.utils.options import opt_analysis
from austrakka.utils.enums.seq import FASTA_UPLOAD_TYPE
from .funcs import add_fasta_submission
from .funcs import add_fastq_submission
from .funcs import take_sample_names
from .funcs import get_sequences
from .funcs import list_sequences


def _check_mutex_group_analysis(group, analysis):
    if group is None and analysis is None:
        raise click.UsageError("Either 'group' or 'analysis' must be provided")
    if group is not None and analysis is not None:
        raise click.UsageError(
            "Both 'group' or 'analysis' cannot be provided simultaneously"
        )


@click.group()
@click.pass_context
def seq(ctx):
    """Commands related to sequences"""
    ctx.creds = ctx.parent.creds


@seq.command('add')
@opt_csv(help='CSV with mapping from Seq_ID to sequence files', required=True)
@opt_seq_type()
def submission_add(
        csv_file: BufferedReader,
        seq_type: str
):
    """
    Upload sequence submission to AusTrakka

    The following CSV mapping fields are required:\n
        For FASTA:\n
            Seq_ID: The sample name in AusTrakka\n
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
@opt_output_dir()
@opt_seq_type()
@opt_read()
@opt_group(default=None, multiple=False, required=False)
@opt_analysis(default=None, required=False)
def get(
        output_dir,
        seq_type: str,
        read: str,
        group_name: str,
        analysis: str,
):
    """Download sequence files to the local drive

    EXAMPLE 1: Download Fastq with both Reads for species SARS-CoV-2

        austrakka seq get -t fastq --species SARS-CoV-2 --outdir ~/Downloads/fastq-files


    EXAMPLE 2: Download Fasta for group Example-Group

        austrakka seq get -t fasta --group-name Example-Group --outdir ~/Downloads/fasta-files


    """
    _check_mutex_group_analysis(group_name, analysis)
    get_sequences(
        output_dir,
        seq_type,
        read,
        group_name,
        analysis,
    )


@seq.command('list')
@table_format_option()
@opt_seq_type(default=None, required=False)
@opt_read()
@opt_group(default=None, multiple=False, required=False)
@opt_analysis(default=None, required=False)
def seq_list(
        out_format: str,
        seq_type: str,
        read: str,
        group_name: str,
        analysis: str,
):
    _check_mutex_group_analysis(group_name, analysis)
    list_sequences(
        out_format,
        seq_type,
        read,
        group_name,
        analysis,
    )
