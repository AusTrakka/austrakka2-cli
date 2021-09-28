import os
import sys

import click
from click.core import Context
from loguru import logger

from .auth import auth
from .user import user
from . import __version__ as VERSION
from .utils import HandleTopLevelParams
from .utils import DEVELOPMENT_ENV

@click.group(cls=HandleTopLevelParams)
@click.option("--uri", show_envvar=True, required=True)
@click.option("--token", show_envvar=True, required=True)
@click.version_option(message="%(prog)s v%(version)s", version=VERSION)
@click.pass_context
def cli(ctx: Context, uri: str, token: str):
    """
    A cli for interfacing with AusTrakka from the command line.
    """
    ctx.creds = {'uri': uri, 'token': token}


cli.add_command(auth)
cli.add_command(user)


def main():
    try:
        # pylint: disable=unexpected-keyword-arg,no-value-for-parameter
        cli(auto_envvar_prefix='AT')
    # pylint: disable=broad-except
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
    sys.exit(1)


if __name__ == '__main__':
    main()
