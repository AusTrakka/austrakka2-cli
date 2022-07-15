import click

from austrakka.utils.output import table_format_option
from austrakka.utils.cmd_filter import hide_admin_cmds
from .funcs import list_projects, add_project
from ...utils.options import *


@click.group()
@click.pass_context
def project(ctx):
    '''Commands related to projects'''
    ctx.creds = ctx.parent.creds


@project.command('add', hidden=hide_admin_cmds())
@opt_abbrev()
@opt_name(help_text="Project name")
@opt_description
@opt_organisation()
def project_add(abbrev, name, description, org):
    '''
    Add a new project to AusTrakka.
    '''
    add_project(abbrev, name, description, org)


@project.command('list')
@table_format_option()
def projects_list(table_format: str):
    '''List projects in AusTrakka'''
    list_projects(table_format)
