import click

from austrakka.utils.output import table_format_option
from .funcs import list_species, add_species
from ...utils.options import *


@click.group()
@click.pass_context
def species(ctx):
    '''Commands related to species'''
    ctx.creds = ctx.parent.creds


@species.command('add')
@opt_abbrev()
@opt_name(help_text="Species name")
@opt_taxon_id
def species_add(abbrev, name, taxon_id):
    '''
    Add a species to AusTrakka.
    '''
    add_species(abbrev, name, taxon_id)


@species.command('list')
@table_format_option()
def species_list(table_format: str):
    '''List species in AusTrakka'''
    list_species(table_format)
