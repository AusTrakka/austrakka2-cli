from typing import List
import click

from austrakka.utils.output import table_format_option
from .funcs import \
    add_proforma, \
    update_proforma, \
    list_proformas, \
    show_proformas, \
    disable_proforma, \
    enable_proforma

from ...utils.options import *


@click.group()
@click.pass_context
def proforma(ctx):
    """Commands related to metadata pro formas"""
    ctx.creds = ctx.parent.creds


@proforma.command('add')
@opt_abbrev()
@opt_name()
@opt_description
@click.option('-s',
              '--species',
              required=False,
              help="Species abbreviations for suggested species for use with this pro forma. "
              "Zero, one, or many species may be specified. "
              "These species may be used to find appropriate pro formas, but will not "
              "constrain use of the pro forma.",
              type=click.STRING,
              multiple=True)
@click.option('-req',
              '--required-field',
              help='Required field in this pro forma; users must populate this field in every '
                   'upload. Multiple fields may be added.',
              type=click.STRING,
              multiple=True)
@click.option('-opt',
              '--optional-field',
              help='Optional field in this pro forma; users may include this field in uploads. '
                   'Multiple fields may be added.',
              type=click.STRING,
              multiple=True)
def proforma_add(
        abbrev: str,
        name: str,
        description: str,
        species: List[str],
        required_field: List[str],
        optional_field: List[str]):
    """
    Add a new pro forma to AusTrakka.
    This will add a new pro forma with a new abbreviation, not a new version.
    """
    add_proforma(
        abbrev,
        name,
        description,
        species,
        required_field,
        optional_field)


@proforma.command('update')
@click.option('-req',
              '--required-field',
              help='Required field in this pro forma; users must populate this field in every '
                   'upload. Multiple fields may be added.',
              type=click.STRING,
              multiple=True)
@click.option('-opt',
              '--optional-field',
              help='Optional field in this pro forma; users may include this field in uploads. '
                   'Multiple fields may be added.',
              type=click.STRING,
              multiple=True)
@click.argument('abbrev', type=click.STRING)
def proforma_update(
        abbrev: str,
        required_field: List[str],
        optional_field: List[str]):
    """
    Update a pro forma with a new set of fields.
    The fields specified by -req and -opt will fully replace the fields in the current version.
    Any fields in the current version but not listed in the update will be removed.
    """
    update_proforma(
        abbrev,
        required_field,
        optional_field)


@proforma.command('list')
@table_format_option()
def proforma_list(table_format: str):
    """List metadata pro formas in AusTrakka"""
    list_proformas(table_format)


@proforma.command('show')
@click.argument('abbrev', type=click.STRING)
# Consider option instead: @opt_abbrev("Abbreviated name of the pro forma")
@table_format_option()
def proforma_show(abbrev: str, table_format: str):
    """
    Show pro forma fields.

    USAGE:
    austrakka proforma show [ABBREV]

    ABBREV should be the abbreviated name of the pro forma.
    Use `austrakka proforma list` for options.
    """
    show_proformas(abbrev, table_format)


@proforma.command('disable')
@click.argument('abbrev', type=click.STRING)
# Consider option instead: @opt_abbrev("Abbreviated name of the pro forma")
def proforma_disable(abbrev: str):
    """
    Disable a pro forma.

    USAGE:
    austrakka proforma disable [ABBREV]

    ABBREV should be the abbreviated name of the pro forma.
    """
    disable_proforma(abbrev)


@proforma.command('enable')
@click.argument('abbrev', type=click.STRING)
# Consider option instead: @opt_abbrev("Abbreviated name of the pro forma")
def proforma_enable(abbrev: str):
    """
    Enable a pro forma.

    USAGE:
    austrakka proforma enable [ABBREV]

    ABBREV should be the abbreviated name of the pro forma.
    """
    enable_proforma(abbrev)
