import click

from austrakka.utils.output import table_format_option
from austrakka.utils.cmd_filter import hide_admin_cmds
from austrakka.utils.options import opt_abbrev
from austrakka.utils.options import opt_name
from austrakka.utils.options import opt_taxon_id
from austrakka.utils.options import opt_is_active
from .funcs import list_species
from .funcs import add_species
from .funcs import update_species


@click.group()
@click.pass_context
def species(ctx):
    '''Commands related to species'''
    ctx.creds = ctx.parent.creds


@species.command('add', hidden=hide_admin_cmds())
@opt_abbrev()
@opt_name(help_text="Species name")
@opt_taxon_id()
@opt_is_active
def species_add(abbrev: str, name: str, taxon_id: str, is_active: bool):
    '''
    Add a species to AusTrakka.
    '''
    add_species(abbrev, name, taxon_id, is_active)


@species.command('update', hidden=hide_admin_cmds())
@click.argument('abbrev', type=str)
@opt_name(help_text="Species name", required=False)
@opt_taxon_id(required=False)
@opt_is_active
def species_update(abbrev: str, name: str, taxon_id: str, is_active: bool):
    '''
    Update a species in AusTrakka.
    '''
    update_species(abbrev, name, taxon_id, is_active)


@species.command('list')
@table_format_option()
def species_list(table_format: str):
    '''List species in AusTrakka'''
    list_species(table_format)
