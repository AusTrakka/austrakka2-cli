from typing import List
import click
from austrakka.components.project.setup.funcs import \
    add_field_project, \
    set_merge_algorithm_project, \
    add_provision_project, get_dataset_provision_list, get_project_field_list, \
    remove_project_field, remove_project_provision, update_project_provision
from austrakka.utils.cmd_filter import hide_admin_cmds
from austrakka.utils.options import \
    opt_field_name, \
    opt_merge_algorithm, \
    opt_field_and_source, \
    opt_abbrev, opt_prov_id
from austrakka.utils.output import table_format_option


# pylint: disable=duplicate-code
@click.group()
@click.pass_context
def setup(ctx):
    """Commands to upload project datasets"""
    ctx.context = ctx.parent.context


@setup.command('add-fields', hidden=hide_admin_cmds())
@opt_abbrev()
@opt_field_and_source()
def project_add_field(abbrev: str, field_source):
    """
    add fields for a given project.
    """
    add_field_project(abbrev, field_source)


@setup.command('remove-fields', hidden=hide_admin_cmds())
@opt_abbrev()
@opt_field_name()
def project_remove_field(abbrev: str, field_names: List[str]):
    """
    disable fields for a given project.
    """
    remove_project_field(abbrev, field_names)


@setup.command('set-merge')
@opt_abbrev()
@opt_merge_algorithm()
def project_set_merge_algo(abbrev: str, merge_algorithm):
    """
    set merge algorithm for a given project
    """
    set_merge_algorithm_project(abbrev, merge_algorithm)


@setup.command('add-provision')
@opt_abbrev()
@opt_field_name()
def project_add_provision(abbrev: str, field_names: List[str]):
    """This will add a project provision"""
    add_provision_project(abbrev, field_names)


@setup.command('remove-provision')
@opt_abbrev()
@opt_prov_id()
def project_remove_provision(abbrev: str, prov_id: str):
    """This will remove a project provision"""
    remove_project_provision(abbrev, prov_id)


@setup.command('update-provision')
@opt_abbrev()
@opt_field_name()
@opt_prov_id()
def project_update_provision(abbrev: str, field_names: List[str], prov_id: str):
    """This will update a project provision"""
    update_project_provision(abbrev, prov_id, field_names)

@setup.command('list-provisions')
@table_format_option()
@opt_abbrev()
def project_list_provisions(abbrev: str, out_format: str):
    """This will list project provisions"""
    get_dataset_provision_list(abbrev, out_format)


@setup.command('list-fields')
@table_format_option()
@opt_abbrev()
def project_list_fields(abbrev: str, out_format: str):
    """This will list project fields"""
    get_project_field_list(abbrev, out_format)
