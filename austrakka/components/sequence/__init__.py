# pylint: disable=redefined-outer-name
from typing import List

import click

from austrakka.utils.output import table_format_option
from austrakka.utils.options import RequiredMutuallyExclusiveOption, opt_seq_type, opt_group_name
from austrakka.utils.options import opt_output_dir
from austrakka.utils.options import opt_sample_id
from austrakka.utils.options import opt_force_mutex_skip
from austrakka.utils.options import opt_skip_mutex_force
from austrakka.utils.options import opt_delete_all
from austrakka.utils.cmd_filter import hide_admin_cmds

from .funcs import take_sample_names
from .funcs import get_sequences
from .funcs import list_sequences
from .funcs import purge_sequence
from .add import add
from .sync import sync



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
    mutually_exclusive=['sample_id'])
@opt_sample_id(
    required=False,
    default=None,
    help='The Seq_IDs of specific sequences to download',
    cls=RequiredMutuallyExclusiveOption,
    mutually_exclusive=['group_name'])
def seq_get(
        output_dir,
        seq_type: str,
        group_name: str,
        sample_id: List[str],
):
    """Download sequence files to the local drive

    EXAMPLE: Download Fasta for group Example-Group

        austrakka seq get -t fasta --group-name Example-Group --outdir ~/Downloads/fasta-files
    """
    get_sequences(
        output_dir,
        seq_type,
        group_name,
        sample_id,
    )


@seq.command('list')
@table_format_option()
@opt_seq_type(default=None, required=False)
@opt_group_name(
    required=False,
    default=None,
    multiple=False,
    cls=RequiredMutuallyExclusiveOption,
    mutually_exclusive=['sample_id'])
@opt_sample_id(
    required=False,
    default=None,
    help='The Seq_IDs of specific sequences to download',
    cls=RequiredMutuallyExclusiveOption,
    mutually_exclusive=['group_name'])
def seq_list(
        out_format: str,
        seq_type: str,
        group_name: str,
        sample_id: List[str],
):
    list_sequences(
        out_format,
        seq_type,
        group_name,
        sample_id
    )


@seq.command('purge', hidden=hide_admin_cmds())
@opt_sample_id(
    help='The id of the sample which needs to have sequences purged.',
    multiple=False
)
@opt_seq_type()
@opt_skip_mutex_force(help="Skip this command if the sample is still active.")
@opt_force_mutex_skip(help="Forcefully purge sequences belonging to the sample "
                           "even if the sample is still active.")
@opt_delete_all(help='Delete active and inactive sequences for the specified sample. '
                     'By default, only inactive sequences are deleted.')
def sequence_purge(
        sample_id: [str],
        seq_type: str,
        skip: bool = False,
        force: bool = False,
        delete_all: bool = False):
    """Purge all sequences associated with the specified sample."""
    purge_sequence(sample_id, seq_type, skip, force, delete_all)
