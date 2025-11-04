# pylint: disable=redefined-outer-name
from io import BufferedReader
import click

from austrakka.utils.options import opt_seq_id, opt_group_name, opt_project, options_seq_id_or_file
from austrakka.utils.option_utils import get_seq_list
from austrakka.utils.option_utils import RequiredMutuallyExclusiveOption
from austrakka.utils.cmd_filter import hide_admin_cmds
from ...utils.option_utils import create_option
from ...utils.output import table_format_option
from ...utils.output import object_format_option
from .funcs import \
    disable_sample, \
    enable_sample, \
    unshare_sample, \
    share_sample, \
    get_groups, \
    show_sample, \
    purge_sample, \
    change_owner


@click.group()
@click.pass_context
def sample(ctx):
    """Commands related to samples"""
    ctx.context = ctx.parent.context

@sample.command('chown',
    hidden=hide_admin_cmds(),
    help="Transfer ownership of samples to another organisation")
@create_option(
    "--old-owner",
    required=True,
    help='Abbreviated name of current owning organisation'
)
@create_option(
    "--new-owner",
    required=True,
    help='Abbreviated name of new owning organisation'
)
@options_seq_id_or_file
def owner_change(old_owner: str, new_owner: str, seq_id: [str], file: BufferedReader):
    seq_ids = get_seq_list(seq_id, file)
    change_owner(old_owner, new_owner, seq_ids)

@sample.command('show', hidden=hide_admin_cmds())
@opt_seq_id(multiple=False)
@object_format_option()
def sample_show(seq_id: str, out_format: str):
    """Show all available information about a sample record."""
    show_sample(seq_id, out_format)


@sample.command('unshare')
@opt_group_name(mutually_exclusive=['project'],
                cls=RequiredMutuallyExclusiveOption,
                required=False,)
@opt_project(mutually_exclusive=['group_name'],
             cls=RequiredMutuallyExclusiveOption,
             required=False, )
@options_seq_id_or_file
def sample_unshare(seq_id: [str], group_name: str, project: str, file: BufferedReader):
    """Unshare a list of sample records with a group."""
    seq_ids = get_seq_list(seq_id, file)
    unshare_sample(group_name, project, seq_ids)

@sample.command('share')
@opt_group_name(cls=RequiredMutuallyExclusiveOption,
                mutually_exclusive=['project'],
                required=False)
@opt_project(mutually_exclusive=['group_name'],
             cls=RequiredMutuallyExclusiveOption,
             required=False,)
@options_seq_id_or_file
def sample_share(seq_id: [str], group_name: str, project: str, file: BufferedReader):
    """Share a list of sample records with a group."""
    seq_ids = get_seq_list(seq_id, file)
    share_sample(group_name, project, seq_ids)

@sample.command('disable')
@options_seq_id_or_file
def sample_disable(seq_id: [str], file: BufferedReader):
    """Disable a sample record. This is a soft delete. 
    The sample record's metadata and sequences will not appear in any projects. 
    Once disabled, it will not be possible to upload metadata or sequences
    to the sample until it is enabled again, or until it has been purged
    from the system."""
    seq_ids = get_seq_list(seq_id, file)
    disable_sample(seq_ids)


@sample.command('groups')
@table_format_option()
@opt_seq_id(multiple=False)
def seq_groups(
        seq_id: str,
        out_format: str
):
    """List the groups that the sample record is in (shared with, or owned by)."""
    get_groups(
        seq_id,
        out_format,
    )


@sample.command('enable')
@options_seq_id_or_file
def sample_enable(seq_id: [str], file: BufferedReader):
    """Enable a sample record. This re-enables a previously disabled sample."""
    seq_ids = get_seq_list(seq_id, file)
    enable_sample(seq_ids)


@sample.command('purge', hidden=hide_admin_cmds())
@opt_seq_id(
    help='The Seq_ID of the sample record to be purged.',
    multiple=False)
def sample_purge(seq_id: str):
    """Purge a sample record. This will purge all metadata including any CSV or Excel
    files used to upload metadata, and including the original upload. If other Seq_IDs were  
    uploaded in the same CSV/Excel files, the other samples will not be purged, but will lose the 
    link to the original CSV/Excel file. This action is irreversible. Any sequences 
    must be purged prior to purging the sample."""
    purge_sample(seq_id)
