import os
import sys
from tempfile import NamedTemporaryFile
from tempfile import gettempdir

import click
from click.core import Context
from loguru import logger

from austrakka.auth import auth
from austrakka.user import user
from austrakka.analysis import analysis
from austrakka.tree import tree
from austrakka.species import species
from austrakka.submission import submission

from austrakka import __version__ as VERSION
from austrakka.utils import HandleTopLevelParams
from austrakka.utils import is_dev_env

CLI_PREFIX = 'AT'
CLI_ENV = 'env'

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(cls=HandleTopLevelParams, context_settings=CONTEXT_SETTINGS)
@click.option("--uri", show_envvar=True, required=True)
@click.option("--token", show_envvar=True, required=True)
@click.option(
    f"--{CLI_ENV}",
    show_envvar=True,
    required=True,
    default='prod',
    show_default=True
)
@click.option(
    '--log',
    show_envvar=True,
    help='Outputs logs to a temporary file',
)
@click.version_option(message="%(prog)s v%(version)s", version=VERSION)
@click.pass_context
def cli(ctx: Context, uri: str, token: str, env: str, log: str):
    """
    A cli for interfacing with AusTrakka from the command line.
    """
    ctx.creds = {'uri': uri, 'token': token}
    logger.remove()
    logger.add(sys.stderr, level='DEBUG' if is_dev_env(env) else 'INFO')
    if log == 'file':
        logger.debug(f'Creating temp file in {gettempdir()}')
        # pylint: disable=consider-using-with
        log_file = NamedTemporaryFile(
            mode='w',
            prefix='austrakka-cli-output-',
            suffix='.log',
            delete=False
        )
        logger.info(f'Redirecting log output to {log_file.name}')
        logger.remove()
        logger.add(log_file.name)


def main():
    try:
        cli.add_command(auth)
        cli.add_command(user)
        cli.add_command(analysis)
        cli.add_command(tree)
        cli.add_command(species)
        cli.add_command(submission)
        # pylint: disable=unexpected-keyword-arg,no-value-for-parameter
        cli(auto_envvar_prefix=CLI_PREFIX)
    except Exception as exc:  # pylint: disable=broad-except
        if is_dev_env(os.environ.get(f"{CLI_PREFIX}_{CLI_ENV.upper()}")):
            logger.exception(exc)
        else:
            logger.error(exc)
        sys.exit(1)
    sys.exit(0)


if __name__ == '__main__':
    main()
