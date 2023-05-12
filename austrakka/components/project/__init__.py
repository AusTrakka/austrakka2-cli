import click
from austrakka.utils.output import table_format_option
from austrakka.utils.cmd_filter import hide_admin_cmds
from austrakka.utils.options import opt_abbrev
from austrakka.utils.options import opt_name
from austrakka.utils.options import opt_description
from austrakka.utils.options import opt_organisation
from austrakka.components.project.funcs import list_projects, add_project


@click.group()
@click.pass_context
def project(ctx):
    '''Commands related to projects'''
    ctx.context = ctx.parent.context


@project.command('add', hidden=hide_admin_cmds())
@opt_abbrev(help="Project Abbreviation")
@opt_name(help="Project name")
@opt_description(required=False)
@opt_organisation(help="Requesting organisation abbreviation", required=False)
def project_add(abbrev: str, name: str, description: str, org: str):
    '''
    Add a new project to AusTrakka.
    '''
    add_project(abbrev, name, description, org)


@project.command('list')
@table_format_option()
def projects_list(out_format: str):
    '''List projects in AusTrakka'''
    list_projects(out_format)
