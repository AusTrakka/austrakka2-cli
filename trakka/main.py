# pylint: disable=expression-not-assigned
import sys
import uuid

import click
from click.core import Context
from loguru import logger

from trakka.utils.context import CxtKey
from trakka.utils.context import TrakkaCxt
from trakka.components.admin import admin
from trakka.components.auth import auth
from trakka.components.user import user
from trakka.components.org import org
from trakka.components.log import log
from trakka.components.project import project
from trakka.components.tree import tree
from trakka.components.metadata import metadata
from trakka.components.sequence import seq
from trakka.components.proforma import proforma
from trakka.components.field import field
from trakka.components.fieldtype import fieldtype
from trakka.components.group import group
from trakka.components.sample import sample
from trakka.components.dashboard import dashboard
from trakka.components.plot import plot
from trakka.components.iam import iam

from trakka import __version__ as VERSION
from trakka import __prog_name__ as PROG_NAME
from trakka.utils.datetimes import LOCAL_TIMEZONE
from trakka.utils.misc import TrakkaCliTopLevel
from trakka.utils.logger import is_debug
from trakka.utils.misc import HELP_OPTS
from trakka.utils.exceptions import FailedResponseException
from trakka.utils.output import log_response
from trakka.utils.logger import setup_logger
from trakka.utils.logger import LOG_LEVEL_INFO
from trakka.utils.logger import LOG_LEVELS
from trakka.utils.cmd_filter import USER, show_admin_cmds
from trakka.utils.version import check_version


CONTEXT_SETTINGS = {"help_option_names": HELP_OPTS}


@click.group(
    cls=TrakkaCliTopLevel, 
    context_settings=CONTEXT_SETTINGS,
    help="""
    A cli for interfacing with Trakka.
    """,
)
@click.option(
    TrakkaCxt.get_option_name(CxtKey.URI), 
    show_envvar=True,
    envvar=TrakkaCxt.get_env_var_names(CxtKey.URI),
    required=True
)
@click.option(
    TrakkaCxt.get_option_name(CxtKey.TOKEN),
    show_envvar=True,
    envvar=TrakkaCxt.get_env_var_names(CxtKey.TOKEN),
    required=True
)
@click.option(
    TrakkaCxt.get_option_name(CxtKey.LOG_LEVEL), 
    show_envvar=True,
    envvar=TrakkaCxt.get_env_var_names(CxtKey.LOG_LEVEL),
    default=LOG_LEVEL_INFO,
    type=click.Choice(LOG_LEVELS),
    show_default=True
)
@click.option(
    TrakkaCxt.get_option_name(CxtKey.TIMEZONE),
    '-tz',
    show_envvar=True,
    envvar=TrakkaCxt.get_env_var_names(CxtKey.TIMEZONE),
    default=LOCAL_TIMEZONE,
    show_default=True,
    help='Timezone to use for any datetime output or parsing. '
         'Can be "local" to use your local timezone, '
         'or a recognised timezone string such as "UTC", "Australia/Perth" or "Europe/Madrid".'
)
@click.option(
    TrakkaCxt.get_option_name(CxtKey.SKIP_CERT_VERIFY),
    show_envvar=True,
    envvar=TrakkaCxt.get_env_var_names(CxtKey.SKIP_CERT_VERIFY),
    required=True,
    default=False,
    show_default=True,
    type=bool,
    help="Skip verification of certificate"
)
@click.option(
    TrakkaCxt.get_option_name(CxtKey.USE_HTTP2), 
    show_envvar=True,
    envvar=TrakkaCxt.get_env_var_names(CxtKey.USE_HTTP2),
    required=True,
    default=False,
    show_default=True,
    type=bool,
    help="Use HTTP2 (experimental)"
)
@click.option(
    TrakkaCxt.get_option_name(CxtKey.SKIP_VERSION_CHECK),
    show_envvar=True,
    envvar=TrakkaCxt.get_env_var_names(CxtKey.SKIP_VERSION_CHECK),
    required=True,
    default=False,
    show_default=True,
    type=bool,
    help="Skip check for new CLI version"
)
@click.option(
    TrakkaCxt.get_option_name(CxtKey.CMD_SET),
    show_envvar=True,
    envvar=TrakkaCxt.get_env_var_names(CxtKey.CMD_SET),
    required=True,
    default=USER,
    show_default=True,
    type=str,
    help="Hide/show admin commands"
)
@click.option(
    '--log',
    'log_var',
    show_envvar=True,
    help='Outputs logs to a temporary file',
)
@click.version_option(message="%(prog)s v%(version)s", version=VERSION, prog_name=PROG_NAME)
@click.pass_context
def cli(
        ctx: Context,
        uri: str,
        token: str,
        log_level: str,
        timezone: str,
        skip_cert_verify: bool,
        use_http2: bool,
        skip_version_check: bool,
        log_var: str,
        cmd_set: str,
):
    ctx.context = {
        CxtKey.URI.value: uri,
        CxtKey.TOKEN.value: token,
        CxtKey.SKIP_CERT_VERIFY.value: skip_cert_verify,
        CxtKey.SKIP_VERSION_CHECK .value: skip_version_check,
        CxtKey.USE_HTTP2.value: use_http2,
        CxtKey.LOG_LEVEL.value: log_level,
        CxtKey.SESSION_ID.value: str(uuid.uuid4()),
        CxtKey.TIMEZONE.value: timezone,
        CxtKey.CMD_SET.value: cmd_set,
    }
    setup_logger(log_level, log_var)
    if not skip_version_check:
        check_version(VERSION)
    TrakkaCxt.check_deprecated_env_vars()


def get_cli():
    cli.add_command(admin) if show_admin_cmds() else None
    cli.add_command(auth)
    cli.add_command(user) if show_admin_cmds() else None
    cli.add_command(org) if show_admin_cmds() else None
    cli.add_command(group)
    cli.add_command(project)
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
    cli.add_command(log) if show_admin_cmds() else None
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
        # Cannot use TrakkaCxt.value here because there is no click context

        if is_debug(TrakkaCxt.get_env_var_value(CxtKey.LOG_LEVEL, '')):
            logger.exception(ex)
        else:
            logger.error(ex)
        sys.exit(1)
    sys.exit(0)


if __name__ == '__main__':
    main()
