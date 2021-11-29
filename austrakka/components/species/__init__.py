import click

from austrakka.utils.output import table_format_option
from .funcs import list_species


@click.group()
@click.pass_context
def species(ctx):
    '''Commands related to species'''
    ctx.creds = ctx.parent.creds


@species.command('list')
@table_format_option()
def species_list(table_format: str):
    '''List species in AusTrakka'''
    list_species(table_format)
