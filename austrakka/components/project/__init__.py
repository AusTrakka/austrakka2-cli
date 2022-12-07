# pylint: disable=expression-not-assigned
from austrakka.utils.output import table_format_option
from austrakka.utils.cmd_filter import hide_admin_cmds, show_admin_cmds
from austrakka.components.project.funcs import list_projects, add_project

from ...utils.options import *


@click.group()
@click.pass_context
def project(ctx):
    '''Commands related to projects'''
    ctx.creds = ctx.parent.creds


@project.command('add', hidden=hide_admin_cmds())
@opt_abbrev()
@opt_name(help="Project name")
@opt_description(required=False)
def project_add(abbrev, name, description):
    '''
    Add a new project to AusTrakka.
    '''
    add_project(abbrev, name, description)


@project.command('list')
@table_format_option()
def projects_list(out_format: str):
    '''List projects in AusTrakka'''
    list_projects(out_format)
