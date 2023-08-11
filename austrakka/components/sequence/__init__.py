# pylint: disable=redefined-outer-name
import click
from click import option

from austrakka.utils.output import table_format_option
from austrakka.utils.options import opt_seq_type, opt_seq_filter
from austrakka.utils.options import opt_output_dir
from austrakka.utils.options import opt_read
from austrakka.utils.options import opt_group
from austrakka.utils.options import opt_sample_id
from austrakka.utils.options import MutuallyExclusiveOption
from austrakka.utils.cmd_filter import hide_admin_cmds

from .funcs import take_sample_names
from .funcs import get_sequences
from .funcs import list_sequences
from .funcs import purge_sequence
from .add import add
from .sync import sync


BY_SAMPLE = 'by-sample'


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
@opt_read()
@opt_group(default=None, multiple=False, required=True)
@opt_seq_filter(multiple=False, required=False)
def get(
        output_dir,
        seq_type: str,
        read: str,
        group_name: str,
        sub_query_type: str,
):
    """Download sequence files to the local drive

    EXAMPLE: Download Fasta for group Example-Group

        austrakka seq get -t fasta --group-name Example-Group --outdir ~/Downloads/fasta-files


    """
    get_sequences(
        output_dir,
        seq_type,
        read,
        group_name,
        sub_query_type,
    )


@seq.command('list')
@table_format_option()
@opt_seq_type(default=None, required=False)
@opt_read()
@opt_group(default=None, multiple=False, required=True)
@opt_seq_filter(multiple=False, required=False)
def seq_list(
        out_format: str,
        seq_type: str,
        read: str,
        group_name: str,
        sub_query_type: str,
):
    list_sequences(
        out_format,
        seq_type,
        read,
        group_name,
        sub_query_type,
    )


@seq.command('purge', hidden=hide_admin_cmds())
@opt_sample_id(
    help='The id of the sample which needs to have sequences purged.',
    multiple=False
)
@option('--skip', cls=MutuallyExclusiveOption,
        help="Skip this command if the sample is still active.",
        mutually_exclusive=["force"],
        is_flag=True)
@option('--force',
        cls=MutuallyExclusiveOption,
        help="Forcefully purge sequences belonging to the sample "
             "even if the sample is still active.",
        mutually_exclusive=["skip"],
        is_flag=True)
def sequence_purge(sample_id: [str], skip: bool = False, force: bool = False):
    """Purge all sequences associated with the specified sample."""
    purge_sequence(sample_id, skip, force)
