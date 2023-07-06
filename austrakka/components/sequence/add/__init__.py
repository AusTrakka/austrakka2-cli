
from io import BufferedReader

import click

from austrakka.utils.options import opt_csv, \
    opt_owner_group_for_record_creation, opt_shared_groups_for_record_creation
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
    
    If no record exists for these Seq_IDs you can first add them with the
    `austrakka metadata add` command, and may use the minimal proforma if
    you wish to specify no metadata other than sample ownership.
    
    Alternatively, if no record exists for these Seq_IDs and all will have
    the same ownership and sharing settings, you can use the --owner-goup 
    and --shared-groups options.
    """
    add_fastq_submission(csv_file)


@add.command('fasta')
@click.argument('fasta_file', type=click.File('rb'))
@opt_owner_group_for_record_creation()
@opt_shared_groups_for_record_creation()
def seq_add_fasta(
        fasta_file: BufferedReader,
        owner_group,
        shared_groups
):
    """
    Upload FASTA submission to AusTrakka

    A single FASTA file should be supplied.
    Contig names must correspond to known Seq_IDs.

    If no record exists for these Seq_IDs you can first add them with the
    `austrakka metadata add` command, and may use the minimal proforma if
    you wish to specify no metadata other than sample ownership.
    
    Alternatively, if no record exists for these Seq_IDs and all will have
    the same ownership and sharing settings, you can use the --owner-group 
    and --shared-groups options.
    """
    if len(shared_groups)>0 and owner_group is None:
        raise ValueError("--shared-groups requires --owner-group")
    # For now we just forbid this completely via this mechanism
    if owner_group is not None and len(shared_groups)==0:
        raise ValueError("Owner group specified but no shared groups; these sequences will not be "
                         "available within any projects. This is not usually what you want. "
                         "If this is deliberate, please manually run "
                         "`austrakka metadata add -p min`, or contact an AusTrakka admin.")
    add_fasta_submission(fasta_file, owner_group, shared_groups)
