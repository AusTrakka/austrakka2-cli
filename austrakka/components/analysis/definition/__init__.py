import click

from austrakka.utils.output import table_format_option
from austrakka.components.analysis.definition.funcs import add_definition
from austrakka.components.analysis.definition.funcs import update_definition
from austrakka.components.analysis.definition.funcs import list_definitions
from austrakka.utils.cmd_filter import hide_admin_cmds
from austrakka.utils.options import opt_name
from austrakka.utils.options import opt_description
from austrakka.utils.options import opt_is_active


@click.group()
@click.pass_context
def definition(ctx):
    """Commands related to analyses"""
    ctx.context = ctx.parent.context


@definition.command('list')
@table_format_option()
def definition_list(out_format: str):
    """List analysis definitions in AusTrakka"""
    list_definitions(out_format)


@definition.command('add', hidden=hide_admin_cmds())
@opt_name()
@opt_description()
@opt_is_active()
def definition_add(
        name: str,
        description: str,
        is_active: bool
):
    """Add analysis definition in AusTrakka"""
    add_definition(name, description, is_active)


@definition.command('update', hidden=hide_admin_cmds())
@click.argument('name', type=str)
@opt_description(required=False)
@opt_is_active(is_update=True)
def definition_update(
        name: str,
        description: str,
        is_active: bool
):
    """Update analysis definition in AusTrakka"""
    update_definition(name, description, is_active)
