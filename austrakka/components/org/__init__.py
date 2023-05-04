import click

from austrakka.utils.output import table_format_option
from austrakka.utils.cmd_filter import hide_admin_cmds
from austrakka.utils.options import opt_name
from austrakka.utils.options import opt_abbrev
from austrakka.utils.options import opt_is_active
from austrakka.utils.options import opt_country
from austrakka.utils.options import opt_state
from .funcs import list_orgs
from .funcs import add_org
from .funcs import update_org


@click.group()
@click.pass_context
def org(ctx):
    '''Commands related to organisations'''
    ctx.context = ctx.parent.context


@org.command('list')
@table_format_option()
def org_list(out_format: str):
    '''List organisations in AusTrakka'''
    list_orgs(out_format)


@org.command('add', hidden=hide_admin_cmds())
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
    '''Add organisations in AusTrakka'''
    add_org(name, abbrev, country, state, is_active)


@org.command('update', hidden=hide_admin_cmds())
@click.argument('abbrev', type=str)
@opt_name(help="Organisation Name", required=False)
@opt_state(required=False)
@opt_country(required=False)
@opt_is_active(is_update=True)
def org_update(
        abbrev: str,
        name: str,
        country: str,
        state: str,
        is_active: bool,
):
    '''Update organisations in AusTrakka'''
    update_org(abbrev, name, country, state, is_active)
