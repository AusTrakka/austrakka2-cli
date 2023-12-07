import click

from austrakka.components.project.field.funcs import add_field_project
from austrakka.utils.cmd_filter import hide_admin_cmds
from austrakka.utils.options import opt_field_name

# pylint: disable=duplicate-code
@click.group()
@click.pass_context
def field(ctx):
    """Commands to upload project datasets"""
    ctx.context = ctx.parent.context


@field.command('add', hidden=hide_admin_cmds())
@click.argument('name', type=str)
@opt_field_name()
def project_add_field(name, field_names):
    '''
    add fields for a given project.
    '''
    add_field_project(name, field_names)
