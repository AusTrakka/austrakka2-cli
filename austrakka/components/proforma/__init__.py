from typing import List

from click_option_group import optgroup
from austrakka.utils.output import table_format_option
from austrakka.utils.cmd_filter import hide_admin_cmds
from .funcs import \
    add_proforma, \
    update_proforma, \
    list_proformas, \
    show_proformas, \
    disable_proforma, \
    enable_proforma, \
    share_proforma, \
    unshare_proforma

from ...utils.options import *


@click.group()
@click.pass_context
def proforma(ctx):
    """Commands related to metadata pro formas"""
    ctx.creds = ctx.parent.creds


@proforma.command('add', hidden=hide_admin_cmds())
@opt_abbrev()
@opt_name()
@opt_description(required=False)
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
        required_field,
        optional_field)


@proforma.command('update', hidden=hide_admin_cmds())
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
def proforma_list(out_format: str):
    """List metadata pro formas in AusTrakka"""
    list_proformas(out_format)


@proforma.command('show')
@click.argument('abbrev', type=click.STRING)
# Consider option instead: @opt_abbrev("Abbreviated name of the pro forma")
@table_format_option()
def proforma_show(abbrev: str, out_format: str):
    """
    Show pro forma fields.

    USAGE:
    austrakka proforma show [ABBREV]

    ABBREV should be the abbreviated name of the pro forma.
    Use `austrakka proforma list` for options.
    """
    show_proformas(abbrev, out_format)


@proforma.command('disable', hidden=hide_admin_cmds())
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


@proforma.command('enable', hidden=hide_admin_cmds())
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


@proforma.command('share', hidden=hide_admin_cmds())
@click.argument('abbrev', type=click.STRING)
@opt_groups()
def proforma_share(abbrev: str, group_names: List[str]):
    """
    Share a pro forma with one or more groups so can see the proforma
    in the `list` operation.

    USAGE:
    austrakka proforma share -g [GROUP NAME] [ABBREV]

    ABBREV should be the abbreviated name of the pro forma.
    """
    share_proforma(abbrev, group_names)


@proforma.command('unshare', hidden=hide_admin_cmds())
@click.argument('abbrev', type=click.STRING)
@opt_groups()
def proforma_unshare(abbrev: str, group_names: List[str]):
    """
    UnShare a pro forma with one or more groups to prevent the proforma
    being returned in the `list` operation.

    USAGE:
    austrakka proforma unshare -g [GROUP NAME] [ABBREV]

    ABBREV should be the abbreviated name of the pro forma.
    """
    unshare_proforma(abbrev, group_names)
