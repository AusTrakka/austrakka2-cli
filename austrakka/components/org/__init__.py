import click

from austrakka.utils.output import table_format_option
from austrakka.utils.cmd_filter import hide_admin_cmds
from austrakka.utils.options import opt_name
from austrakka.utils.options import opt_abbrev
from .funcs import list_orgs
from .funcs import add_org
from .funcs import update_org


@click.group()
@click.pass_context
def org(ctx):
    '''Commands related to organisations'''
    ctx.creds = ctx.parent.creds


@org.command('list')
@table_format_option()
def org_list(table_format: str):
    '''List organisations in AusTrakka'''
    list_orgs(table_format)


@org.command('add', hidden=hide_admin_cmds())
@opt_name(help_text="Organisation Name")
@opt_abbrev(help_text="Organisation Abbreviation")
@click.option('--state', type=str, default=None)
@click.option('--country', type=str, required=True)
@click.option('--is-active/--not-active', default=True, type=bool)
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
@click.argument('identifier', type=int)
@opt_name(help_text="Organisation Name", required=False)
@click.option('--state', type=str)
@click.option('--country', type=str)
@click.option('--is-active/--not-active', default=True, type=bool)
def org_update(
        identifier: int,
        name: str,
        country: str,
        state: str,
        is_active: bool,
):
    '''Update organisations in AusTrakka'''
    update_org(identifier, name, country, state, is_active)
