import click

from austrakka.utils.output import table_format_option
from .funcs import list_proformas, show_proformas


@click.group()
@click.pass_context
def proforma(ctx):
    """Commands related to metadata pro formas"""
    ctx.creds = ctx.parent.creds


@proforma.command('list')
@table_format_option()
def proforma_list(table_format: str):
    """List metadata pro formas in AusTrakka"""
    list_proformas(table_format)


@proforma.command('show')
@click.argument('abbrev', type=click.STRING)
@table_format_option()
def proforma_show(abbrev: str, table_format: str):
    """
    Show pro forma fields.

    USAGE:
    austrakka proforma show [NAME]

    NAME should be the abbreviated name of the pro forma.
    """
    show_proformas(abbrev, table_format)
