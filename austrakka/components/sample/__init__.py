# pylint: disable=redefined-outer-name
from io import BufferedReader
import click

from austrakka.utils.options import opt_sample_id, opt_group_name
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
@opt_sample_id(multiple=False)
@object_format_option()
def sample_show(sample_id: str, out_format: str):
    show_sample(sample_id, out_format)


@sample.command('unshare')
@opt_group_name()
@opt_sample_id(
    help='The id of the sample to be unshared. Multiple ids can be specified.'
         'Eg. -s sample1 -s sample2')
def sample_unshare(sample_id: [str], group_name: str):
    """Unshare a list of samples with a group."""
    unshare_sample(sample_id, group_name)


@sample.command('share')
@opt_group_name()
@opt_sample_id(
    help='The id of the sample to be shared. Multiple ids can be specified.'
         'Eg. -s sample1 -s sample2')
def sample_share(sample_id: [str], group_name: str):
    """Share a list of samples with a group."""
    share_sample(sample_id, group_name)


@sample.command('disable')
@opt_sample_id(
    help='The id of the sample to be removed. Multiple ids can be specified.'
    'Eg. -s sample1 -s sample2')
def sample_disable(sample_id: [str]):
    """Disable a sample. This is like a soft delete. It may be purged
    after 30 days. Once disabled, it will not be possible to upload metadata or sequences
    to the sample until it is enabled again, or until it has been purged
    from the system."""
    disable_sample(sample_id)


@sample.command('groups')
@table_format_option()
@opt_sample_id(multiple=False)
def seq_groups(
        sample_id: str,
        out_format: str
):
    """List the groups that the sample is in (shared with, or owned by)."""
    get_groups(
        sample_id,
        out_format,
    )


@sample.command('enable')
@opt_sample_id(
    help='The id of the sample to be re-enable. Multiple ids can be specified.'
    'Eg. -s sample1 -s sample2')
def sample_enable(sample_id: [str]):
    """Enable a sample. This re-enables a previously disabled sample."""
    enable_sample(sample_id)


@sample.command('purge', hidden=hide_admin_cmds())
@opt_sample_id(
    help='The id of the sample to be purged.',
    multiple=False)
def sample_purge(sample_id: str):
    """Purge a sample. This will purge all metadata including the original CSV 
    file which it was uploaded from. If more than one sample was uploaded from 
    the same CSV file, the other samples will not be purged, but will lose the 
    link to the original CSV file. This action is irreversible. Any sequences 
    must be purged prior to purging the sample."""
    purge_sample(sample_id)
