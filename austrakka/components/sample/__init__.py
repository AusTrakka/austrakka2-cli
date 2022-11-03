# pylint: disable=redefined-outer-name
from io import BufferedReader
import click

from .funcs import disable_sample


@click.group()
@click.pass_context
def sample(ctx):
    """Commands related to samples"""
    ctx.creds = ctx.parent.creds


@sample.command('disable')
@click.option('-s',
              '--sample-id',
              help='The id of the sample to be removed. Multiple ids can be specified.'
                   'Eg. -s sample1 -s sample2',
              type=click.STRING,
              multiple=True)
def sample_disable(sample_id: [str]):
    """Disable a sample. This is like a soft delete. It will be purged
    after 30 days. To re-enable, you will have to contact an admin.
    Once disabled, it will not be possible to upload metadata or sequences
    to the sample until it is enabled again, or until it has been purged
    from the system."""
    disable_sample(sample_id)
