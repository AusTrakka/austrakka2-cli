import click

from austrakka.utils.output import table_format_option
from austrakka.components.analysis.definition.funcs import add_definition
from austrakka.components.analysis.definition.funcs import update_definition
from austrakka.components.analysis.definition.funcs import list_definitions
from austrakka.utils.cmd_filter import hide_admin_cmds
from austrakka.utils.options import opt_name
from austrakka.utils.options import opt_description
from austrakka.utils.options import opt_is_active
from austrakka import __prog_name__ as PROG_NAME


@click.group()
@click.pass_context
def definition(ctx):
    """Commands related to analysis definitions"""
    ctx.context = ctx.parent.context


@definition.command('list', help=f'List analysis definitions in {PROG_NAME}')
@table_format_option()
def definition_list(out_format: str):
    list_definitions(out_format)


@definition.command(
        'add', 
        hidden=hide_admin_cmds(),
        help=f'Add analysis definition in {PROG_NAME}'
)
@opt_name()
@opt_description()
@opt_is_active()
def definition_add(
        name: str,
        description: str,
        is_active: bool
):
    add_definition(name, description, is_active)


@definition.command(
        'update',
        hidden=hide_admin_cmds(),
        help=f'Update analysis definition in {PROG_NAME}'
)
@click.argument('name', type=str)
@opt_description(required=False)
@opt_is_active(is_update=True)
def definition_update(
        name: str,
        description: str,
        is_active: bool
):
    update_definition(name, description, is_active)
