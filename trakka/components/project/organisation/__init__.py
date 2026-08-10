from typing import List

import click

from trakka.components.project.organisation.funcs import get_project_organisation_list, \
    add_project_organisation, \
    remove_project_organisation
from trakka.utils.cmd_filter import hide_admin_cmds
from trakka.utils.options import opt_organisation, opt_identifier
from trakka.utils.output import table_format_option


@click.group()
@click.pass_context
def organisation(ctx):
    """Commands to manage project organisations"""
    ctx.context = ctx.parent.context

@organisation.command('list')
@table_format_option()
@opt_identifier(help="Project abbrev or global id", var_name="identifier")
def project_list_organisations(identifier: str, out_format: str):
    """Lists all organisations in the project"""
    get_project_organisation_list(identifier, out_format)

@organisation.command('add', hidden=hide_admin_cmds())
@opt_identifier(help="Project abbrev or global id", var_name="identifier")
@opt_organisation(multiple=True, help="Organisations related to this project")
def project_add_organisation(identifier: str, org: List[str]):
    """Adds new organisations to the project"""
    add_project_organisation(identifier, org)

@organisation.command('remove', hidden=hide_admin_cmds())
@opt_identifier(help="Project abbrev or global id", var_name="identifier")
@opt_organisation(multiple=True, help="Organisations related to this project")
def project_remove_organisation(identifier: str, org: List[str]):
    """Removes organisations from the project"""
    remove_project_organisation(identifier, org)
