import os
import sys

import click
from click.core import Context
from loguru import logger

from .components.auth import auth
from .components.user import user
from .components.org import org
from .components.project import project
from .components.analysis import analysis
from .components.tree import tree
from .components.species import species
from .components.metadata import metadata
from .components.sequence import seq
from .components.static import static

from . import __version__ as VERSION
from .utils.misc import HandleTopLevelParams
from .utils.misc import is_dev_env
from .utils.misc import HELP_OPTS
from .utils.exceptions import FailedResponseException
from .utils.output import log_response
from .utils.logger import setup_logger

CLI_PREFIX = 'AT'
CLI_ENV = 'env'

CONTEXT_SETTINGS = dict(help_option_names=HELP_OPTS)


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
    A cli for interfacing with AusTrakka.
    """
    ctx.creds = {'uri': uri, 'token': token}
    setup_logger(env, log)


def main():
    try:
        cli.add_command(auth)
        cli.add_command(user)
        cli.add_command(org)
        cli.add_command(project)
        cli.add_command(analysis)
        cli.add_command(tree)
        cli.add_command(species)
        cli.add_command(metadata)
        cli.add_command(seq)
        cli.add_command(static)
        # pylint: disable=unexpected-keyword-arg,no-value-for-parameter
        cli(auto_envvar_prefix=CLI_PREFIX)
    except FailedResponseException as ex:
        log_response(ex.parsed_resp)
    except Exception as ex:  # pylint: disable=broad-except
        if is_dev_env(os.environ.get(f"{CLI_PREFIX}_{CLI_ENV.upper()}")):
            logger.exception(ex)
        else:
            logger.error(ex)
        sys.exit(1)
    sys.exit(0)


if __name__ == '__main__':
    main()
