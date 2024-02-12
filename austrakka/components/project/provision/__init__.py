from typing import List
import click
from .funcs import \
    add_provision_project, get_dataset_provision_list, \
    remove_project_provision, update_project_provision
from austrakka.utils.options import \
    opt_field_name, \
    opt_abbrev, opt_prov_id
from austrakka.utils.output import table_format_option


@click.group()
@click.pass_context
def provision(ctx):
    """Commands to manage project view provisions. This is used for defining the fields 
    that are part of a project view. Many views can be defined for a project but the 
    fields that each provision references must have already been added to the project. 
    See the 'project field' commands for managing fields in a project."""
    ctx.context = ctx.parent.context


@provision.command('add')
@opt_abbrev()
@opt_field_name()
def project_add_provision(abbrev: str, field_names: List[str]):
    """This will add a project provision"""
    add_provision_project(abbrev, field_names)


@provision.command('remove')
@opt_abbrev()
@opt_prov_id()
def project_remove_provision(abbrev: str, prov_id: str):
    """This will remove a project provision"""
    remove_project_provision(abbrev, prov_id)


@provision.command('update')
@opt_abbrev()
@opt_field_name()
@opt_prov_id()
def project_update_provision(abbrev: str, field_names: List[str], prov_id: str):
    """This will update a project provision"""
    update_project_provision(abbrev, prov_id, field_names)


@provision.command('list')
@table_format_option()
@opt_abbrev()
def project_list_provisions(abbrev: str, out_format: str):
    """This will list project provisions"""
    get_dataset_provision_list(abbrev, out_format)
