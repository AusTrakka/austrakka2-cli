# pylint: disable=expression-not-assigned
import click

from austrakka import __prog_name__ as PROG_NAME
from austrakka.utils.output import table_format_option
from austrakka.utils.output import object_format_option
from austrakka.utils.cmd_filter import hide_admin_cmds
from austrakka.utils.options import opt_abbrev, \
    opt_is_active, \
    opt_type, \
    opt_view_type, opt_project_client_type, opt_merge_algorithm
from austrakka.utils.options import opt_name
from austrakka.utils.options import opt_dashboard_name
from austrakka.utils.options import opt_description
from austrakka.utils.options import opt_organisation
from .funcs import list_projects, \
    add_project, \
    update_project, \
    set_dashboard, \
    get_dashboard, \
    show_project_settings, \
    set_project_type

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


@project.command(
        'add', 
        hidden=hide_admin_cmds(),
        help=f'Add a new project to {PROG_NAME}.'
)
@opt_abbrev(help="Project Abbreviation")
@opt_name(help="Project name")
@opt_description(required=False)
@opt_organisation(help="Requesting organisation abbreviation", required=False)
@opt_dashboard_name(required=False)
@opt_type(required=False)
@opt_project_client_type()
@opt_merge_algorithm()
def project_add(
        abbrev: str,
        name: str,
        description: str,
        org: str,
        dashboard_name: str,
        project_type: str,
        client_type: str,
        merge_algo: str):
    add_project(abbrev,
                name,
                description,
                org,
                dashboard_name,
                project_type,
                client_type,
                merge_algo)


@project.command(
        'update', 
        hidden=hide_admin_cmds(),
        help=f'Update an existing project in {PROG_NAME}.',
)
@click.argument('project-abbrev', type=str)
@opt_name(help="New project name", required=False)
@opt_description(help="New project description", required=False)
@opt_is_active(help="Set project active status", is_update=True, required=False)
@opt_organisation(help="New requesting organisation abbreviation", required=False)
@opt_dashboard_name(help="New dashboard", required=False)
@opt_project_client_type(required=False)
@opt_merge_algorithm(required=False)
@opt_type(help="New project type", required=False)
def project_update(
        project_abbrev: str,
        name: str,
        description: str,
        is_active: bool,
        org: str,
        dashboard_name: str,
        project_type: str,
        client_type: str,
        merge_algo: str):
    update_project(project_abbrev,
                   name,
                   description,
                   is_active,
                   org,
                   dashboard_name,
                   project_type,
                   client_type,
                   merge_algo)


@project.command('set-dashboard', hidden=hide_admin_cmds())
@opt_name(help="name of a known dashboard")
@click.argument('project-abbrev', type=str)
def dashboard_set(project_abbrev: str, name: str):
    '''
    Assign a dashboard to a project.
    '''
    set_dashboard(project_abbrev, name)


@project.command('get-dashboard', hidden=hide_admin_cmds())
@click.argument('project-abbrev', type=str)
@object_format_option()
def dashboard_get(project_abbrev: str, out_format: str):
    '''
    Get the name of the dashboard currently assigned to a project.
    '''
    get_dashboard(project_abbrev, out_format)


@project.command('list', help=f'List projects in {PROG_NAME}')
@opt_view_type()
@table_format_option()
def projects_list(view_type: str,out_format: str):
    list_projects(view_type, out_format)

@project.command('settings')
@click.argument('project-abbrev', type=str)
@object_format_option()
def project_settings(project_abbrev: str, out_format: str):
    '''Show project settings'''
    show_project_settings(project_abbrev, out_format)
    
@project.command('set-type')
@click.argument('project-abbrev', type=str)
@opt_type()
def project_set_type(project_abbrev: str, project_type: str):
    '''Set a type for a project'''
    set_project_type(project_abbrev, project_type)
