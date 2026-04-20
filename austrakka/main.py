# pylint: disable=expression-not-assigned
import os
import sys
import uuid

import click
from click.core import Context
from loguru import logger

from austrakka.utils.config import get_server_info_or_create
from austrakka.utils.context import CxtKey
from austrakka.utils.context import AusTrakkaCxt
from austrakka.components.admin import admin
from austrakka.components.auth import auth
from austrakka.components.user import user
from austrakka.components.org import org
from austrakka.components.log import log
from austrakka.components.project import project
from austrakka.components.tree import tree
from austrakka.components.metadata import metadata
from austrakka.components.sequence import seq
from austrakka.components.proforma import proforma
from austrakka.components.field import field
from austrakka.components.fieldtype import fieldtype
from austrakka.components.group import group
from austrakka.components.sample import sample
from austrakka.components.dashboard import dashboard
from austrakka.components.plot import plot
from austrakka.components.iam import iam

from austrakka import __version__ as VERSION
from austrakka import __prog_name__ as PROG_NAME
from austrakka.utils.datetimes import LOCAL_TIMEZONE
from austrakka.utils.misc import AusTrakkaCliTopLevel
from austrakka.utils.logger import is_debug
from austrakka.utils.misc import HELP_OPTS
from austrakka.utils.exceptions import FailedResponseException
from austrakka.utils.output import log_response
from austrakka.utils.logger import setup_logger
from austrakka.utils.logger import LOG_LEVEL_INFO
from austrakka.utils.logger import LOG_LEVELS
from austrakka.utils.cmd_filter import show_admin_cmds
from austrakka.utils.version import check_version


CONTEXT_SETTINGS = {"help_option_names": HELP_OPTS}


@click.group(
    cls=AusTrakkaCliTopLevel, 
    context_settings=CONTEXT_SETTINGS,
    help=f"""
    A cli for interfacing with {PROG_NAME}.
    """,
)
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
    default=LOG_LEVEL_INFO,
    type=click.Choice(LOG_LEVELS),
    show_default=True
)
@click.option(
    AusTrakkaCxt.get_option_name(CxtKey.TIMEZONE),
    '-tz',
    show_envvar=True,
    envvar=AusTrakkaCxt.get_env_var_name(CxtKey.TIMEZONE),
    default=LOCAL_TIMEZONE,
    show_default=True,
    help='Timezone to use for any datetime output or parsing. '
         'Can be "local" to use your local timezone, '
         'or a recognised timezone string such as "UTC", "Australia/Perth" or "Europe/Madrid".'
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
    help=f"Skip check for new {PROG_NAME} CLI version"
)
@click.option(
    '--log',
    'log_var',
    show_envvar=True,
    help='Outputs logs to a temporary file',
)
@click.version_option(message="%(prog)s v%(version)s", version=VERSION, prog_name=PROG_NAME.lower())
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
    }
    setup_logger(log_level, log_var)
    if not skip_version_check:
        server_info = get_server_info_or_create(
            uri,
            skip_cert_verify,
        )
        if server_info is None:
            check_version(VERSION)
        else:
            logger.debug("Not checking for new CLI updates as server is not"
                         + " rolling.")


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
        # Cannot use AusTrakkaCxt.value here because there is no click context
        if is_debug(os.getenv(AusTrakkaCxt.get_env_var_name(CxtKey.LOG_LEVEL), '')):
            logger.exception(ex)
        else:
            logger.error(ex)
        sys.exit(1)
    sys.exit(0)


if __name__ == '__main__':
    main()
