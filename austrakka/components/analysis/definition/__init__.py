from typing import List

import click

from austrakka.components.analysis.definition.funcs import add_definition
from austrakka.components.analysis.definition.funcs import update_definition
from austrakka.utils.cmd_filter import hide_admin_cmds
from austrakka.utils.options import opt_species
from austrakka.utils.options import opt_name
from austrakka.utils.options import opt_description
from austrakka.utils.options import opt_is_active


@click.group()
@click.pass_context
def definition(ctx):
    """Commands related to analyses"""
    ctx.creds = ctx.parent.creds


@definition.command('add', hidden=hide_admin_cmds())
@opt_name()
@opt_description()
@opt_species(multiple=True)
@opt_is_active()
def definition_add(
        name: str,
        description: str,
        species: List[str],
        is_active: bool
):
    """Add analysis definition in AusTrakka"""
    add_definition(name, description, species, is_active)


@definition.command('update', hidden=hide_admin_cmds())
@click.argument('name', type=str)
@opt_description(required=False)
@opt_species(required=False, multiple=True)
@opt_is_active(is_update=True)
def definition_update(
        name: str,
        description: str,
        species: List[str],
        is_active: bool
):
    """Update analysis definition in AusTrakka"""
    update_definition(name, description, species, is_active)
