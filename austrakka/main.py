import os
import sys

import click
from loguru import logger

from . import __version__ as VERSION
from .utils import IgnoreRequiredWithHelp
from .utils import DEVELOPMENT_ENV

from austrakka.auth import auth
from austrakka.user import user


@click.group(cls=IgnoreRequiredWithHelp)
@click.option("--api-key", show_envvar=True, required=True)
@click.option("--uri", show_envvar=True, required=True)
@click.option("--token", show_envvar=True, required=True)
@click.version_option(message="%(prog)s v%(version)s", version=VERSION)
@click.help_option("-h", "--help")
@click.pass_context
def cli(ctx, api_key, uri, token):
    """
    A cli for interfacing with AusTrakka from the command line.
    """
    ctx.creds = {'api_key': api_key, 'uri': uri, 'token': token}


cli.add_command(auth)
cli.add_command(user)

def main():
    try:
        cli(auto_envvar_prefix='AT')
    except Exception as exc:
        if os.environ.get("AUSTRAKKA_ENV") == DEVELOPMENT_ENV:
            logger.exception(exc)
            logger.remove()
            logger.add(sys.stderr, level="DEBUG")
        else:
            logger.error(exc)
            # Set default log level to INFO
            logger.remove()
            logger.add(sys.stderr, level="INFO")
    exit(1)

if __name__ == '__main__':
    main()
