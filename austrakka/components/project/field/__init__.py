from typing import List
import click

from austrakka.utils.cmd_filter import hide_admin_cmds
from austrakka.utils.output import table_format_option

from austrakka.utils.options import \
    opt_field_name, \
    opt_field_and_source
from .funcs import \
    add_field_project, \
    get_project_field_list, \
    remove_project_field


# pylint: disable=(duplicate-code)
@click.group()
@click.pass_context
def field(ctx):
    """Commands to manage project fields"""
    ctx.context = ctx.parent.context


@field.command('add', hidden=hide_admin_cmds())
@click.argument('project-abbrev', type=str)
@opt_field_and_source()
def project_add_field(project_abbrev: str, field_source):
    """
    Add fields to a given project.
    """
    add_field_project(project_abbrev, field_source)


@field.command('remove', hidden=hide_admin_cmds())
@click.argument('project-abbrev', type=str)
@opt_field_name()
def project_remove_field(project_abbrev: str, field_names: List[str]):
    """
    Remove fields from a given project; fields will no longer be displayed in project metadata.
    """
    remove_project_field(project_abbrev, field_names)


@field.command('list')
@table_format_option()
@click.argument('project-abbrev', type=str)
def project_list_fields(project_abbrev: str, out_format: str):
    """List project fields for a given project"""
    get_project_field_list(project_abbrev, out_format)
