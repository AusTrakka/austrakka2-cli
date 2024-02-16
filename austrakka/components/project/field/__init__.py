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
    """Commands to manage project fields for analysis metadata"""
    ctx.context = ctx.parent.context


@field.command('add', hidden=hide_admin_cmds())
@click.argument('abbrev', type=str)
@opt_field_and_source()
def project_add_field(abbrev: str, field_source):
    """
    add fields for a given project.
    """
    add_field_project(abbrev, field_source)


@field.command('remove', hidden=hide_admin_cmds())
@click.argument('abbrev', type=str)
@opt_field_name()
def project_remove_field(abbrev: str, field_names: List[str]):
    """
    disable fields for a given project.
    """
    remove_project_field(abbrev, field_names)


@field.command('list')
@table_format_option()
@click.argument('abbrev', type=str)
def project_list_fields(abbrev: str, out_format: str):
    """This will list project fields"""
    get_project_field_list(abbrev, out_format)
