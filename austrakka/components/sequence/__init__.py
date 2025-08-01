# pylint: disable=redefined-outer-name
from typing import List

import click

from austrakka.utils.output import table_format_option

from austrakka.utils.option_utils import RequiredMutuallyExclusiveOption
from austrakka.utils.options import opt_seq_type
from austrakka.utils.options import opt_group_name
from austrakka.utils.options import opt_output_dir
from austrakka.utils.options import opt_seq_id
from austrakka.utils.options import opt_force_mutex_skip
from austrakka.utils.options import opt_skip_mutex_force
from austrakka.utils.options import opt_delete_all

from austrakka.utils.cmd_filter import hide_admin_cmds

from .funcs import get_sequences
from .funcs import list_sequences
from .funcs import purge_sequence
from .add import add
from .sync import sync
from ...utils.enums.seq import convert_to_seq_type


@click.group()
@click.pass_context
def seq(ctx):
    """Commands related to sequences"""
    ctx.context = ctx.parent.context


seq.add_command(add)
seq.add_command(sync)


@seq.command('get')
@opt_output_dir()
@opt_seq_type()
@opt_group_name(
    required=False,
    default=None,
    multiple=False,
    cls=RequiredMutuallyExclusiveOption,
    mutually_exclusive=['seq_id'])
@opt_seq_id(
    required=False,
    default=None,
    help='The Seq_IDs of specific sequences to download',
    cls=RequiredMutuallyExclusiveOption,
    mutually_exclusive=['group_name'])
def seq_get(
        output_dir,
        seq_type: str,
        group_name: str,
        seq_id: List[str],
):
    """Download sequence files to the local drive

    EXAMPLE: Download Fasta for group Example-Group

        austrakka seq get -t fasta --group-name Example-Group --outdir ~/Downloads/fasta-files
    """
    seq_type_enum = convert_to_seq_type(seq_type)
    
    # Pass the enum value instead of the string
    get_sequences(
        output_dir,
        seq_type_enum,
        group_name,
        seq_id,
    )


@seq.command('list')
@table_format_option()
@opt_seq_type(default=None, required=False)
@opt_group_name(
    required=False,
    default=None,
    multiple=False,
    cls=RequiredMutuallyExclusiveOption,
    mutually_exclusive=['seq_id'])
@opt_seq_id(
    required=False,
    default=None,
    help='The Seq_IDs of specific sequences to download',
    cls=RequiredMutuallyExclusiveOption,
    mutually_exclusive=['group_name'])
def seq_list(
        out_format: str,
        seq_type: str,
        group_name: str,
        seq_id: List[str],
):
    """List sequences for a group or sample"""
    seq_type_enum = convert_to_seq_type(seq_type)
    
    list_sequences(
        out_format,
        group_name,
        seq_type_enum,
        seq_id
    )


@seq.command('purge', hidden=hide_admin_cmds())
@opt_seq_id(
    help='The Seq_ID of the sample which needs to have sequences purged.',
    multiple=False
)
@opt_seq_type()
@opt_skip_mutex_force(help="Skip this command if the sample is still active.")
@opt_force_mutex_skip(help="Forcefully purge sequences belonging to the sample "
                           "even if the sample is still active.")
@opt_delete_all(help='Delete active and inactive sequences for the specified sample. '
                     'By default, only inactive sequences are deleted.')
def sequence_purge(
        seq_id: [str],
        seq_type: str,
        skip: bool = False,
        force: bool = False,
        delete_all: bool = False):
    """Purge all sequences associated with the specified Seq_ID."""
    seq_type_enum = convert_to_seq_type(seq_type)
    purge_sequence(seq_id, seq_type_enum, skip, force, delete_all)
