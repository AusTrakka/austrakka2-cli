# pylint: disable=redefined-outer-name
import click

from .metadata import metadata
from .seq import seq


@click.group()
@click.pass_context
def submission(ctx):
    """Commands related to submissions"""
    ctx.creds = ctx.parent.creds


submission.add_command(metadata)
submission.add_command(seq)