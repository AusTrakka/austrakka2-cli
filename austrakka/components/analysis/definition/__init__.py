from typing import List

import click

from austrakka.components.analysis.definition.funcs import add_definition
from austrakka.utils.options import opt_species
from austrakka.utils.options import opt_name
from austrakka.utils.options import opt_description
from austrakka.utils.options import opt_is_active


@click.group()
@click.pass_context
def definition(ctx):
    """Commands related to analyses"""
    ctx.creds = ctx.parent.creds


@definition.command('add')
@opt_name()
@opt_description()
@opt_species(multiple=True)
@opt_is_active
def definition_add(
        name: str,
        description: str,
        species: List[str],
        is_active: bool
):
    """Add analysis definition in AusTrakka"""
    add_definition(name, description, species, is_active)
