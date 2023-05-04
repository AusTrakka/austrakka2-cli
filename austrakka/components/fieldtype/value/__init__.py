from typing import List

import click

from austrakka.utils.cmd_filter import hide_admin_cmds
from austrakka.components.fieldtype.value.funcs import add_fieldtype_values
from austrakka.components.fieldtype.value.funcs import remove_fieldtype_values
from austrakka.utils.options import opt_fieldtype_value


@click.group()
@click.pass_context
def value(ctx):
    """Commands related to fieldtype values"""
    ctx.context = ctx.parent.context


@value.command('add', hidden=hide_admin_cmds())
@click.argument('name', type=str)
@opt_fieldtype_value()
def add_value(name: str, values: List[str]):
    """
    Add valid values for this fieldtype.
    """
    add_fieldtype_values(name, values)


@value.command('remove', hidden=hide_admin_cmds())
@click.argument('name', type=str)
@opt_fieldtype_value()
def remove_value(name, values: List[str]):
    """
    Remove valid values for this fieldtype.
    """
    remove_fieldtype_values(name, values)
