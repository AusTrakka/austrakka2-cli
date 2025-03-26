from io import BufferedReader
from typing import Union

import click

from austrakka.utils.enums.seq import SeqType
from austrakka.utils.options import opt_force_mutex_skip
from austrakka.utils.options import opt_skip_mutex_force
from austrakka.utils.options import opt_owner
from austrakka.utils.options import opt_share
from austrakka import __prog_name__ as PROG_NAME
from ..funcs import add_fasta_cns_submission
from ..funcs import add_sequence_submission

METADATA_ADD_HELP_TEXT = """
    If no record exists for these Seq_IDs you can either provide an owner group
    with --owner and a shared group with --share to create the samples if
    you wish to specify no metadata other than sample ownership. Otherwise, 
    the `austrakka metadata add` command can be used prior to sequence upload.
"""


@click.group()
@click.pass_context
def add(ctx):
    """Commands to upload sequences"""
    ctx.context = ctx.parent.context


@add.command(SeqType.FASTQ_ILL_PE.value, help=f"""
    Upload paired-end Illumina FASTQ data to {PROG_NAME}

    The following CSV mapping fields are required:\n
            Seq_ID: The sample name in {PROG_NAME}\n
            filepath1: The local path of the first read file to be uploaded\n
            filepath2: The local path of the second read file to be uploaded

    {METADATA_ADD_HELP_TEXT}
""")
@click.argument('csv_file', type=click.File('rb'))
@opt_skip_mutex_force(
    help="For each sample, skip upload if the sample has existing sequences of the same type.")
@opt_force_mutex_skip(
    help="Upload sequences and supersede any existing sequences of the same type.")
@opt_owner()
@opt_share()
# pylint: disable=invalid-name
def seq_add_fastq_ill_PE(
        csv_file: BufferedReader,
        skip: bool = False,
        force: bool = False,
        owner_group: Union[str, None] = None,
        shared_group: Union[str, None] = None,
):
    add_sequence_submission(SeqType.FASTQ_ILL_PE, csv_file, skip, force, owner_group, shared_group)


@add.command(SeqType.FASTQ_ILL_SE.value, help=f"""
    Upload single-end Illumina FASTQ data to {PROG_NAME}

    The following CSV mapping fields are required:\n
            Seq_ID: The sample name in {PROG_NAME}\n
            filepath: The local path of the file to be uploaded

    {METADATA_ADD_HELP_TEXT}
""")
@click.argument('csv_file', type=click.File('rb'))
@opt_skip_mutex_force(
    help="For each sample, skip upload if the sample has existing sequences of the same type.")
@opt_force_mutex_skip(
    help="Upload sequences and supersede any existing sequences of the same type.")
@opt_owner()
@opt_share()
# pylint: disable=invalid-name
def seq_add_fastq_ill_SE(
        csv_file: BufferedReader,
        skip: bool = False,
        force: bool = False,
        owner_group: Union[str, None] = None,
        shared_group: Union[str, None] = None,
):
    add_sequence_submission(SeqType.FASTQ_ILL_SE, csv_file, skip, force, owner_group, shared_group)


@add.command(SeqType.FASTQ_ONT.value, help=f"""
    Upload Oxford Nanopore FASTQ data to {PROG_NAME}

    The following CSV mapping fields are required:\n
            Seq_ID: The sample name in {PROG_NAME}\n
            filepath: The local path of the file to be uploaded
    
    {METADATA_ADD_HELP_TEXT}
""")
@click.argument('csv_file', type=click.File('rb'))
@opt_skip_mutex_force(
    help="For each sample, skip upload if the sample has existing sequences of the same type.")
@opt_force_mutex_skip(
    help="Upload sequences and supersede any existing sequences of the same type.")
@opt_owner()
@opt_share()
def seq_add_fastq_ont(
        csv_file: BufferedReader,
        skip: bool = False,
        force: bool = False,
        owner_group: Union[str, None] = None,
        shared_group: Union[str, None] = None,
):
    add_sequence_submission(SeqType.FASTQ_ONT, csv_file, skip, force, owner_group, shared_group)


@add.command(SeqType.FASTA_CNS.value, help=f"""
    Upload consensus FASTA sequences to {PROG_NAME}.

    A single FASTA file should be supplied.
    Multiple samples can be included in the same file.
    Contig names must correspond to known Seq_IDs.

    {METADATA_ADD_HELP_TEXT}
""")
@click.argument('fasta_file', type=click.File('rb'))
@opt_skip_mutex_force(
    help="For each sample, skip upload if the sample has existing sequences of the same type.")
@opt_force_mutex_skip(
    help="Upload sequences and supersede any existing sequences of the same type.")
@opt_owner()
@opt_share()
def seq_add_fasta_cns(
        fasta_file: BufferedReader,
        skip: bool = False,
        force: bool = False,
        owner_group: Union[str, None] = None,
        shared_group: Union[str, None] = None,
):
    # FASTA-CNS is a special case as the CLI does the work of splitting the file,
    # and there is no CSV
    add_fasta_cns_submission(fasta_file, skip, force, owner_group, shared_group)


@add.command(SeqType.FASTA_ASM.value, help=f"""
    Upload FASTA assembly sequences to {PROG_NAME}

    The following CSV mapping fields are required:\n
            Seq_ID: The sample name in {PROG_NAME}\n
            filepath: The local path of the file to be uploaded

    {METADATA_ADD_HELP_TEXT}
""")
@click.argument('csv_file', type=click.File('rb'))
@opt_skip_mutex_force(
    help="For each sample, skip upload if the sample has existing sequences of the same type.")
@opt_force_mutex_skip(
    help="Upload sequences and supersede any existing sequences of the same type.")
@opt_owner()
@opt_share()
def seq_add_fasta_asm(
        csv_file: BufferedReader,
        skip: bool = False,
        force: bool = False,
        owner_group: Union[str, None] = None,
        shared_group: Union[str, None] = None,
):
    add_sequence_submission(SeqType.FASTA_ASM, csv_file, skip, force, owner_group, shared_group)
