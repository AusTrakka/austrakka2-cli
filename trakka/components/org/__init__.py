# pylint: disable=expression-not-assigned
import click

from trakka.utils.output import table_format_option
from trakka.utils.cmd_filter import hide_admin_cmds
from trakka.utils.options import opt_name, opt_show_disabled
from trakka.utils.options import opt_abbrev
from trakka.utils.options import opt_is_active
from trakka.utils.options import opt_country
from trakka.utils.options import opt_state
from trakka.utils.privilege import ORG_RESOURCE
from trakka.components.iam.privilege import privilege_subcommands
from trakka.components.log import log_subcommands
from trakka.components.org.field import field
from trakka.utils.cmd_filter import show_admin_cmds
from .funcs import list_orgs, disable_org, enable_org
from .funcs import add_org
from .funcs import update_org
from .metadata import metadata


@click.group()
@click.pass_context
def org(ctx):
    '''Commands related to organisations'''
    ctx.context = ctx.parent.context

org.add_command(privilege_subcommands(ORG_RESOURCE))
org.add_command(log_subcommands(ORG_RESOURCE))
org.add_command(field) if show_admin_cmds() else None
org.add_command(metadata)

@org.command('list', help="List organisations")
@opt_show_disabled(help="Show disabled organisations", required=False)
@table_format_option()
def org_list(out_format: str, show_disabled: bool):
    list_orgs(out_format, show_disabled)


@org.command('add', hidden=hide_admin_cmds(), help="Add organisation")
@opt_name(help="Organisation Name")
@opt_abbrev(help="Organisation Abbreviation")
@opt_state(required=False)
@opt_country(required=False)
@opt_is_active()
def org_add(
    name: str,
    abbrev: str,
    country: str,
    state: str,
    is_active: bool,
):
    add_org(name, abbrev, country, state, is_active)


@org.command('update', hidden=hide_admin_cmds(), help="Update organisation")
@click.argument('org-abbrev', type=str)
@opt_name(help="Organisation Name", required=False)
@opt_state(required=False)
@opt_country(required=False)
@opt_is_active(is_update=True)
def org_update(
        org_abbrev: str,
        name: str,
        country: str,
        state: str
):
    update_org(org_abbrev, name, country, state)

@org.command('disable', hidden=hide_admin_cmds(), help="Disable organisation")
@click.argument('org-abbrev', type=str)
def org_disable(org_abbrev: str):
    disable_org(org_abbrev)

@org.command('enable', hidden=hide_admin_cmds(), help="Enable organisation")
@click.argument('org-abbrev', type=str)
def org_enable(org_abbrev: str):
    enable_org(org_abbrev)
