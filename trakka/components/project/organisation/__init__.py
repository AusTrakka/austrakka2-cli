from typing import List

import click

from trakka.components.project.organisation.funcs import get_project_organisation_list, add_project_organisation, \
    remove_project_organisation
from trakka.utils.cmd_filter import hide_admin_cmds
from trakka.utils.options import opt_project_organisation
from trakka.utils.output import table_format_option


@click.group()
@click.pass_context
def organisation(ctx):
    """Commands to manage project organisations"""
    ctx.context = ctx.parent.context


@organisation.command('list')
@table_format_option()
@click.argument('project-identifier', type=click.STRING)
def project_list_organisations(project_identifier: str, out_format: str):
    """Lists all organisations in the project"""
    get_project_organisation_list(project_identifier, out_format)

@organisation.command('add', hidden=hide_admin_cmds())
@click.argument('project-identifier', type=click.STRING)
@opt_project_organisation()
def project_add_organisation(project_identifier: str, organisation_names: List[str]):
    """Adds new organisations to the project"""
    add_project_organisation(project_identifier, organisation_names)

@organisation.command('remove', hidden=hide_admin_cmds())
@click.argument('project-identifier', type=click.STRING)
@opt_project_organisation()
def project_remove_organisation(project_identifier: str, organisation_names: List[str]):
    """Removes organisations from the project"""
    remove_project_organisation(project_identifier, organisation_names)