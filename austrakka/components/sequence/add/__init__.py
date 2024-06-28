
from io import BufferedReader

import click

from austrakka.utils.enums.seq import SeqType
from austrakka.utils.options import opt_csv
from austrakka.utils.options import opt_force_mutex_skip, opt_skip_mutex_force
from ..funcs import add_fasta_cns_submission
from ..funcs import add_sequence_submission

@click.group()
@click.pass_context
def add(ctx):
    """Commands to upload sequences"""
    ctx.context = ctx.parent.context


@add.command(SeqType.FASTQ_ILL_PE.value)
@click.argument('csv_file', type=click.File('rb'))
@opt_skip_mutex_force(
    help="For each sample, skip upload if the sample has existing sequences of the same type.")
@opt_force_mutex_skip(
    help="Upload sequences and supersede any existing sequences of the same type.")
# pylint: disable=invalid-name
def seq_add_fastq_ill_PE(
        csv_file: BufferedReader, skip: bool = False, force: bool = False
):
    """
    Upload paired-end Illumina FASTQ data to AusTrakka

    The following CSV mapping fields are required:\n
            Seq_ID: The sample name in AusTrakka\n
            filepath1: The local path of the first read file to be uploaded\n
            filepath2: The local path of the second read file to be uploaded
    """
    add_sequence_submission(SeqType.FASTQ_ILL_PE, csv_file, skip, force)

@add.command(SeqType.FASTQ_ILL_SE.value)
@click.argument('csv_file', type=click.File('rb'))
@opt_skip_mutex_force(
    help="For each sample, skip upload if the sample has existing sequences of the same type.")
@opt_force_mutex_skip(
    help="Upload sequences and supersede any existing sequences of the same type.")
# pylint: disable=invalid-name
def seq_add_fastq_ill_SE(
        csv_file: BufferedReader, skip: bool = False, force: bool = False
):
    """
    Upload single-end Illumina FASTQ data to AusTrakka

    The following CSV mapping fields are required:\n
            Seq_ID: The sample name in AusTrakka\n
            filepath: The local path of the file to be uploaded
    """
    add_sequence_submission(SeqType.FASTQ_ILL_SE, csv_file, skip, force)

@add.command(SeqType.FASTQ_ONT.value)
@click.argument('csv_file', type=click.File('rb'))
@opt_skip_mutex_force(
    help="For each sample, skip upload if the sample has existing sequences of the same type.")
@opt_force_mutex_skip(
    help="Upload sequences and supersede any existing sequences of the same type.")
def seq_add_fastq_ont(
        csv_file: BufferedReader, skip: bool = False, force: bool = False
):
    """
    Upload Oxford Nanopore FASTQ data to AusTrakka

    The following CSV mapping fields are required:\n
            Seq_ID: The sample name in AusTrakka\n
            filepath: The local path of the file to be uploaded
    """
    add_sequence_submission(SeqType.FASTQ_ONT, csv_file, skip, force)

@add.command(SeqType.FASTA_CNS.value)
@click.argument('fasta_file', type=click.File('rb'))
@opt_skip_mutex_force(
    help="For each sample, skip upload if the sample has existing sequences of the same type.")
@opt_force_mutex_skip(
    help="Upload sequences and supersede any existing sequences of the same type.")
def seq_add_fasta_cns(
        fasta_file: BufferedReader, skip: bool = False, force: bool = False
):
    """
    Upload consensus FASTA sequences to AusTrakka.

    A single FASTA file should be supplied.
    Multiple samples can be included in the same file.
    Contig names must correspond to known Seq_IDs.

    If no record exists for these Seq_IDs you can first add them with the
    `austrakka metadata add` command, and may use the minimal proforma if
    you wish to specify no metadata other than sample ownership.
    """
    # FASTA-CNS is a special case as the CLI does the work of splitting the file,
    # and there is no CSV
    add_fasta_cns_submission(fasta_file, skip, force)

@add.command(SeqType.FASTA_ASM.value)
@click.argument('csv_file', type=click.File('rb'))
@opt_skip_mutex_force(
    help="For each sample, skip upload if the sample has existing sequences of the same type.")
@opt_force_mutex_skip(
    help="Upload sequences and supersede any existing sequences of the same type.")
def seq_add_fasta_asm(
        csv_file: BufferedReader, skip: bool = False, force: bool = False
):
    """
    Upload FASTA assembly sequences to AusTrakka

    The following CSV mapping fields are required:\n
            Seq_ID: The sample name in AusTrakka\n
            filepath: The local path of the file to be uploaded
    """
    add_sequence_submission(SeqType.FASTA_ASM, csv_file, skip, force)
