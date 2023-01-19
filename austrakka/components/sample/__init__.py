# pylint: disable=redefined-outer-name
from io import BufferedReader
import click

from austrakka.utils.options import opt_sample_id
from .funcs import disable_sample, enable_sample


@click.group()
@click.pass_context
def sample(ctx):
    """Commands related to samples"""
    ctx.creds = ctx.parent.creds


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


@sample.command('enable')
@opt_sample_id(
    help='The id of the sample to be re-enable. Multiple ids can be specified.'
    'Eg. -s sample1 -s sample2')
def sample_enable(sample_id: [str]):
    """Enable a sample. This re-enables a previously disabled sample."""
    enable_sample(sample_id)
