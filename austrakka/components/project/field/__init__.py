import click

from austrakka.utils.output import table_format_option
from austrakka.utils.cmd_filter import hide_admin_cmds
from austrakka.components.project.field.funcs import set_field_project
from austrakka.components.project.field.funcs import unset_field_project
from austrakka.components.project.field.funcs import display_field_project
from austrakka.utils.options import opt_field_name


@click.group()
@click.pass_context
def field(ctx):
    """Commands related to project fields"""
    ctx.creds = ctx.parent.creds


@field.command('add', hidden=hide_admin_cmds())
@click.argument('abbrev', type=str)
@opt_field_name()
def project_set_field(abbrev, field_names):
    """
    Set fields to show for this project.
    """
    set_field_project(abbrev, field_names)


@field.command('remove', hidden=hide_admin_cmds())
@click.argument('abbrev', type=str)
@opt_field_name()
def project_unset_field(abbrev, field_names):
    """
    Unset fields to show for this project.
    """
    unset_field_project(abbrev, field_names)


@field.command('list', hidden=hide_admin_cmds())
@click.argument('abbrev', type=str)
@table_format_option()
def project_display_field(abbrev: str, table_format: str):
    """
    Unset fields to show for this project.
    """
    display_field_project(abbrev, table_format)
