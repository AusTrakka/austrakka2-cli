from typing import List
import click

from trakka.components.proforma.funcs import list_entities, share_entities, unshare_entities
from trakka.utils.output import table_format_option
from trakka.utils.cmd_filter import hide_admin_cmds
from trakka.utils.options import *
from trakka.utils.privilege import ORG_RESOURCE, PROJECT_RESOURCE


@click.group()
@click.pass_context
def project(ctx):
    """Commands related to project shared proformas"""
    ctx.context = ctx.parent.context


@project.command('list', hidden=hide_admin_cmds())
@opt_identifier(help="Proforma identifier")
@table_format_option()
def proforma_list_projects(identifier: str, out_format: str):
    '''
    List projects a proforma is shared with
    '''
    list_entities(identifier, PROJECT_RESOURCE, out_format)


@project.command('share', hidden=hide_admin_cmds())
@opt_identifier(help="Proforma identifier")
@opt_identifier(
        option_name="-p", 
        var_name="projects",
        help="Project identifier",
        required=True,
        multiple=True,
)
def proforma_share_projects(identifier: str, projects: List[str]):
    '''
    Share proforma with projects
    '''
    share_entities(identifier, PROJECT_RESOURCE, projects)


@project.command('unshare', hidden=hide_admin_cmds())
@opt_identifier(help="Proforma identifier")
@opt_identifier(
        option_name="-p", 
        var_name="projects",
        help="Project identifier",
        required=True,
        multiple=True,
)
def proforma_unshare_projects(identifier: str, projects: List[str]):
    '''
    Unshare proforma with projects
    '''
    unshare_entities(identifier, PROJECT_RESOURCE, projects)

