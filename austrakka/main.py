import os
import sys

import click
from click.core import Context
from loguru import logger

from austrakka.auth import auth
from austrakka.user import user
from austrakka.analysis import analysis
from austrakka.tree import tree

from austrakka import __version__ as VERSION
from austrakka.utils import HandleTopLevelParams
from austrakka.utils import is_dev_env

CLI_PREFIX = 'AT'
CLI_ENV = 'env'


@click.group(cls=HandleTopLevelParams)
@click.option("--uri", show_envvar=True, required=True)
@click.option("--token", show_envvar=True, required=True)
@click.option(
    f"--{CLI_ENV}",
    show_envvar=True,
    required=True,
    default='prod',
    show_default=True
)
@click.version_option(message="%(prog)s v%(version)s", version=VERSION)
@click.pass_context
def cli(ctx: Context, uri: str, token: str, env: str):
    """
    A cli for interfacing with AusTrakka from the command line.
    """
    ctx.creds = {'uri': uri, 'token': token}
    logger.remove()
    logger.add(sys.stderr, level='DEBUG' if is_dev_env(env) else 'INFO')


def main():
    try:
        cli.add_command(auth)
        cli.add_command(user)
        cli.add_command(analysis)
        cli.add_command(tree)
        # pylint: disable=unexpected-keyword-arg,no-value-for-parameter
        cli(auto_envvar_prefix=CLI_PREFIX)
    except Exception as exc:  # pylint: disable=broad-except
        if is_dev_env(os.environ.get(f"{CLI_PREFIX}_{CLI_ENV.upper()}")):
            logger.exception(exc)
        else:
            logger.error(exc)
    sys.exit(1)


if __name__ == '__main__':
    main()
