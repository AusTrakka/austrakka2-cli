# pylint: disable=redefined-outer-name
from io import BufferedReader
import click

from austrakka.utils.options import opt_seq_id, opt_group_name
from austrakka.utils.cmd_filter import hide_admin_cmds
from ...utils.output import table_format_option
from ...utils.output import object_format_option
from .funcs import \
    disable_sample, \
    enable_sample, \
    unshare_sample, \
    share_sample, \
    get_groups, \
    show_sample, \
    purge_sample


@click.group()
@click.pass_context
def sample(ctx):
    """Commands related to samples"""
    ctx.context = ctx.parent.context

@sample.command('show', hidden=hide_admin_cmds())
@opt_seq_id(multiple=False)
@object_format_option()
def sample_show(seq_id: str, out_format: str):
    """Show all available information about a sample record."""
    show_sample(seq_id, out_format)


@sample.command('unshare')
@opt_group_name()
@opt_seq_id(
    help='The Seq_ID of the sample record(s) to be unshared. Multiple Seq_IDs can be specified.'
         'Eg. -s sample1 -s sample2')
def sample_unshare(seq_id: [str], group_name: str):
    """Unshare a list of sample records with a group."""
    unshare_sample(seq_id, group_name)


@sample.command('share')
@opt_group_name()
@opt_seq_id(
    help='The Seq_ID of the sample record(s) to be shared. Multiple Seq_IDs can be specified.'
         'Eg. -s sample1 -s sample2')
def sample_share(seq_id: [str], group_name: str):
    """Share a list of sample records with a group."""
    share_sample(seq_id, group_name)


@sample.command('disable')
@opt_seq_id(
    help='The Seq_ID of the sample record(s) to be removed. Multiple Seq_IDs can be specified.'
    'Eg. -s sample1 -s sample2')
def sample_disable(seq_id: [str]):
    """Disable a sample record. This is a soft delete. 
    The sample record's metadata and sequences will not appear in any projects. 
    Once disabled, it will not be possible to upload metadata or sequences
    to the sample until it is enabled again, or until it has been purged
    from the system."""
    disable_sample(seq_id)


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
@opt_seq_id(
    help='The Seq_ID of the sample record(s) to be re-enabled. Multiple Seq_IDs can be specified.'
    'Eg. -s sample1 -s sample2')
def sample_enable(seq_id: [str]):
    """Enable a sample record. This re-enables a previously disabled sample."""
    enable_sample(seq_id)


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
