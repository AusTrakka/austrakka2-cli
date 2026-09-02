from typing import List
import click

from trakka.components.proforma.funcs import list_entities, share_entities, unshare_entities
from trakka.utils.output import table_format_option
from trakka.utils.cmd_filter import hide_admin_cmds
from trakka.utils.options import *
from trakka.utils.privilege import ORG_RESOURCE


@click.group()
@click.pass_context
def org(ctx):
    """Commands related to organisation shared proformas"""
    ctx.context = ctx.parent.context


@org.command('list', hidden=hide_admin_cmds())
@opt_identifier(help="Proforma identifier")
@table_format_option()
def proforma_list_orgs(identifier: str, out_format: str):
    '''
    List organisations a proforma is shared with
    '''
    list_entities(identifier, ORG_RESOURCE, out_format)


@org.command('share', hidden=hide_admin_cmds())
@opt_identifier(help="Proforma identifier")
@opt_identifier(
        option_name="-o", 
        var_name="orgs",
        help="Org identifier",
        required=True,
        multiple=True,
)
def proforma_share_orgs(identifier: str, orgs: List[str]):
    '''
    Share proforma with organisations
    '''
    share_entities(identifier, ORG_RESOURCE, orgs)


@org.command('unshare', hidden=hide_admin_cmds())
@opt_identifier(help="Proforma identifier")
@opt_identifier(
        option_name="-o", 
        var_name="orgs",
        help="Org identifier",
        required=True,
        multiple=True,
)
def proforma_unshare_orgs(identifier: str, orgs: List[str]):
    '''
    Unshare proforma with organisations
    '''
    unshare_entities(identifier, ORG_RESOURCE, orgs)
