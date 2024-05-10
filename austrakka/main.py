# pylint: disable=expression-not-assigned
import os
import sys

import click
from click.core import Context
from loguru import logger

from austrakka.utils.context import CxtKey
from .components.auth import auth
from .components.user import user
from .components.org import org
from .components.project import project
from .components.analysis import analysis
from .components.tree import tree
from .components.metadata import metadata
from .components.sequence import seq
from .components.proforma import proforma
from .components.field import field
from .components.fieldtype import fieldtype
from .components.group import group
from .components.sample import sample
from .components.widget import widget
from .components.dashboard import dashboard
from .components.plot import plot

from . import __version__ as VERSION
from .utils.misc import AusTrakkaCliTopLevel
from .utils.logger import is_debug
from .utils.misc import HELP_OPTS
from .utils.exceptions import FailedResponseException
from .utils.output import log_response
from .utils.logger import setup_logger
from .utils.logger import LOG_LEVEL_INFO
from .utils.logger import LOG_LEVELS
from .utils.cmd_filter import show_admin_cmds
from .utils.version import check_version

CLI_PREFIX = 'AT'
CLI_LOG_LEVEL = 'LOG_LEVEL'

CONTEXT_SETTINGS = {"help_option_names": HELP_OPTS}


# NOTE: envvar below needs to be explicitly specified despite using
# auto_envvar_prefix due to limitations with CliRunner tests
@click.group(cls=AusTrakkaCliTopLevel, context_settings=CONTEXT_SETTINGS)
@click.option(
    f"--{CxtKey.CTX_URI.value}",
    show_envvar=True,
    envvar='AT_URI',
    required=True
)
@click.option(
    f"--{CxtKey.CTX_TOKEN.value}",
    show_envvar=True,
    envvar='AT_TOKEN',
    required=True
)
@click.option(
    "--log-level",
    show_envvar=True,
    envvar=f"{CLI_PREFIX}_{CLI_LOG_LEVEL}",
    required=True,
    default=LOG_LEVEL_INFO,
    type=click.Choice(LOG_LEVELS),
    show_default=True
)
@click.option(
    f"--{CxtKey.CTX_VERIFY_CERT.value}",
    show_envvar=True,
    required=True,
    default=True,
    show_default=True,
    type=bool,
    help="Skip verification of certificate"
)
@click.option(
    f"--{CxtKey.CTX_USE_HTTP2.value}",
    show_envvar=True,
    required=True,
    default=False,
    show_default=True,
    type=bool,
    help="Use HTTP2 (experimental)"
)
@click.option(
    '--log',
    show_envvar=True,
    help='Outputs logs to a temporary file',
)
@click.version_option(message="%(prog)s v%(version)s", version=VERSION)
@click.pass_context
def cli(
        ctx: Context,
        uri: str,
        token: str,
        log_level: str,
        log: str,
        verify_cert: bool,
        use_http2: bool,
):
    """
    A cli for interfacing with AusTrakka.
    """
    ctx.context = {
        CxtKey.CTX_URI.value: uri,
        CxtKey.CTX_TOKEN.value: token,
        CxtKey.CTX_VERIFY_CERT.value: verify_cert,
        CxtKey.CTX_USE_HTTP2.value: use_http2,
    }
    setup_logger(log_level, log)
    check_version(VERSION)


def get_cli():
    cli.add_command(auth)
    cli.add_command(user) if show_admin_cmds() else None
    cli.add_command(org) if show_admin_cmds() else None
    cli.add_command(group)
    cli.add_command(project)
    cli.add_command(analysis)
    cli.add_command(tree)
    cli.add_command(plot) if show_admin_cmds() else None
    cli.add_command(widget) if show_admin_cmds() else None
    cli.add_command(dashboard) if show_admin_cmds() else None
    cli.add_command(metadata)
    cli.add_command(sample)
    cli.add_command(seq)
    cli.add_command(proforma)
    cli.add_command(field)
    cli.add_command(fieldtype)
    return cli


def main():
    try:
        get_cli()
        # pylint: disable=unexpected-keyword-arg,no-value-for-parameter
        cli(auto_envvar_prefix=CLI_PREFIX)
    except FailedResponseException as ex:
        logger.error("Request failed")
        log_response(ex.parsed_resp)
        sys.exit(1)
    except Exception as ex:  # pylint: disable=broad-except
        if is_debug(os.environ.get(f"{CLI_PREFIX}_{CLI_LOG_LEVEL}")):
            logger.exception(ex)
        else:
            logger.error(ex)
        sys.exit(1)
    sys.exit(0)


if __name__ == '__main__':
    main()
