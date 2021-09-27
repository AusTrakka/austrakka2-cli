import os
import sys

import click
from loguru import logger

from . import __version__ as VERSION
from .utils import CatchAllExceptions


@click.group(cls=CatchAllExceptions)
@click.option("--api-key", envvar='AUSTRAKKA_API_KEY', show_default=True)
@click.option("--uri", envvar='AUSTRAKKA_URI')
@click.version_option(message="%(prog)s v%(version)s", version=VERSION)
@click.help_option("-h", "--help")
@click.pass_context
def cli(ctx, api_key, uri):
    """
    A cli for interfacing with AusTrakka from the command line.
    """
    ctx.creds = {"api_key": api_key, 'uri': uri}

if __name__ == "__main__":
    cli()
