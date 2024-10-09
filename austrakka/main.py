# pylint: disable=expression-not-assigned
import os
import sys

import click
from click.core import Context
from loguru import logger

from austrakka.utils.context import CxtKey
from austrakka.utils.context import AusTrakkaCxt
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
from .components.dashboard import dashboard
from .components.plot import plot
from .components.iam import iam

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


CONTEXT_SETTINGS = {"help_option_names": HELP_OPTS}


@click.group(cls=AusTrakkaCliTopLevel, context_settings=CONTEXT_SETTINGS)
@click.option(
    AusTrakkaCxt.get_option_name(CxtKey.URI), 
    show_envvar=True,
    envvar=AusTrakkaCxt.get_env_var_name(CxtKey.URI),
    required=True
)
@click.option(
    AusTrakkaCxt.get_option_name(CxtKey.TOKEN),
    show_envvar=True,
    envvar=AusTrakkaCxt.get_env_var_name(CxtKey.TOKEN),
    required=True
)
@click.option(
    AusTrakkaCxt.get_option_name(CxtKey.LOG_LEVEL), 
    show_envvar=True,
    envvar=AusTrakkaCxt.get_env_var_name(CxtKey.LOG_LEVEL),
    required=True,
    default=LOG_LEVEL_INFO,
    type=click.Choice(LOG_LEVELS),
    show_default=True
)
@click.option(
    AusTrakkaCxt.get_option_name(CxtKey.SKIP_CERT_VERIFY),
    show_envvar=True,
    envvar=AusTrakkaCxt.get_env_var_name(CxtKey.SKIP_CERT_VERIFY),
    required=True,
    default=False,
    show_default=True,
    type=bool,
    help="Skip verification of certificate"
)
@click.option(
    AusTrakkaCxt.get_option_name(CxtKey.USE_HTTP2), 
    show_envvar=True,
    envvar=AusTrakkaCxt.get_env_var_name(CxtKey.USE_HTTP2),
    required=True,
    default=False,
    show_default=True,
    type=bool,
    help="Use HTTP2 (experimental)"
)
@click.option(
    AusTrakkaCxt.get_option_name(CxtKey.SKIP_VERSION_CHECK),
    show_envvar=True,
    envvar=AusTrakkaCxt.get_env_var_name(CxtKey.SKIP_VERSION_CHECK),
    required=True,
    default=False,
    show_default=True,
    type=bool,
    help="Skip check for new AusTrakka CLI version"
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
        skip_cert_verify: bool,
        use_http2: bool,
        skip_version_check: bool,
        log: str,
):
    """
    A cli for interfacing with AusTrakka.
    """
    ctx.context = {
        CxtKey.URI.value: uri,
        CxtKey.TOKEN.value: token,
        CxtKey.SKIP_CERT_VERIFY.value: skip_cert_verify,
        CxtKey.SKIP_VERSION_CHECK .value: skip_version_check,
        CxtKey.USE_HTTP2.value: use_http2,
        CxtKey.LOG_LEVEL.value: log_level,
    }
    setup_logger(log_level, log)
    if not skip_version_check:
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
    cli.add_command(dashboard) if show_admin_cmds() else None
    cli.add_command(metadata)
    cli.add_command(sample)
    cli.add_command(seq)
    cli.add_command(proforma)
    cli.add_command(field)
    cli.add_command(fieldtype)
    cli.add_command(iam) if show_admin_cmds() else None
    return cli


def main():
    try:
        # pylint: disable=no-value-for-parameter
        get_cli()()
    except FailedResponseException as ex:
        logger.error("Request failed")
        log_response(ex.parsed_resp)
        sys.exit(1)
    except Exception as ex:  # pylint: disable=broad-except
        # Cannot use AusTrakkaCxt.value here because there is no click context
        if is_debug(os.getenv(AusTrakkaCxt.get_env_var_name(CxtKey.LOG_LEVEL), '')):
            logger.exception(ex)
        else:
            logger.error(ex)
        sys.exit(1)
    sys.exit(0)


if __name__ == '__main__':
    main()
