# pylint: disable=expression-not-assigned
import click
from austrakka.utils.output import table_format_option
from austrakka.utils.output import object_format_option
from austrakka.utils.cmd_filter import hide_admin_cmds
from austrakka.utils.options import opt_abbrev, opt_is_active
from austrakka.utils.options import opt_name
from austrakka.utils.options import opt_dashboard_name
from austrakka.utils.options import opt_description
from austrakka.utils.options import opt_organisation
from .funcs import list_projects, \
    add_project, \
    update_project, \
    set_dashboard, \
    get_dashboard, \
    show_project_settings

from .dataset import dataset
from .field import field
from .provision import provision
from .metadata import metadata


@click.group()
@click.pass_context
def project(ctx):
    """Commands related to projects"""
    ctx.context = ctx.parent.context


project.add_command(field)
project.add_command(provision)
project.add_command(metadata)
project.add_command(dataset)


@project.command('add', hidden=hide_admin_cmds())
@opt_abbrev(help="Project Abbreviation")
@opt_name(help="Project name")
@opt_description(required=False)
@opt_organisation(help="Requesting organisation abbreviation", required=False)
@opt_dashboard_name(required=False)
def project_add(
        abbrev: str,
        name: str,
        description: str,
        org: str,
        dashboard_name: str):
    '''
    Add a new project to AusTrakka.
    '''
    add_project(abbrev, name, description, org, dashboard_name)


@project.command('update', hidden=hide_admin_cmds())
@click.argument('project-abbreviation', type=str)
@opt_abbrev(help="New project abbreviation", required=False)
@opt_name(help="New project name", required=False)
@opt_description(help="New project description", required=False)
@opt_is_active(help="Set project active status", is_update=True, required=False)
@opt_organisation(help="New requesting organisation abbreviation", required=False)
@opt_dashboard_name(help="New dashboard", required=False)
def project_update(
        project_abbreviation: str,
        abbrev: str,
        name: str,
        description: str,
        is_active: bool,
        org: str,
        dashboard_name: str):
    '''
    Update an existing project in AusTrakka.
    '''
    update_project(project_abbreviation, abbrev, name, description, is_active, org, dashboard_name)


@project.command('set-dashboard', hidden=hide_admin_cmds())
@opt_name(help="name of a known dashboard")
@click.argument('project-id', type=int)
def dashboard_set(project_id: int, name: str):
    '''
    Assign a dashboard to a project.
    '''
    set_dashboard(project_id, name)


@project.command('get-dashboard', hidden=hide_admin_cmds())
@click.argument('project-id', type=int)
@table_format_option()
def dashboard_get(project_id: int, out_format: str):
    '''
    Get all widgets of the dashboard currently assigned to a project.
    '''
    get_dashboard(project_id, out_format)


@project.command('list')
@table_format_option()
def projects_list(out_format: str):
    '''List projects in AusTrakka'''
    list_projects(out_format)

@project.command('settings')
@click.argument('abbrev', type=str)
@object_format_option()
def project_settings(abbrev: str, out_format: str):
    '''Show project settings'''
    show_project_settings(abbrev, out_format)
