import click

from austrakka.utils.output import table_format_option
from austrakka.utils.cmd_filter import hide_admin_cmds
from .funcs import list_projects, \
    add_project, \
    set_field_project, \
    unset_field_project, \
    display_field_project

from ...utils.options import *


@click.group()
@click.pass_context
def project(ctx):
    '''Commands related to projects'''
    ctx.creds = ctx.parent.creds


@project.command('add', hidden=hide_admin_cmds())
@opt_abbrev()
@opt_name(help_text="Project name")
@opt_description(required=False)
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


@project.command('set-field', hidden=hide_admin_cmds())
@click.argument('abbrev', type=str)
@opt_field_name()
def project_set_field(abbrev, field_names):
    '''
    Set fields to show for this project.
    '''
    set_field_project(abbrev, field_names)


@project.command('unset-field', hidden=hide_admin_cmds())
@click.argument('abbrev', type=str)
@opt_field_name()
def project_unset_field(abbrev, field_names):
    '''
    Unset fields to show for this project.
    '''
    unset_field_project(abbrev, field_names)


@project.command('display-fields', hidden=hide_admin_cmds())
@click.argument('abbrev', type=str)
@table_format_option()
def project_display_field(abbrev: str, table_format: str):
    '''
    Unset fields to show for this project.
    '''
    display_field_project(abbrev, table_format)
