from typing import List

import click

from austrakka.utils.output import table_format_option
from austrakka.utils.cmd_filter import hide_admin_cmds
from .funcs import \
    add_proforma, \
    update_proforma, \
    list_proformas, \
    show_proforma, \
    disable_proforma, \
    enable_proforma, \
    share_proforma, \
    unshare_proforma, \
    list_groups_proforma, \
    attach_proforma, \
    generate_proforma, \
    pull_proforma

from ...utils.options import *


@click.group()
@click.pass_context
def proforma(ctx):
    """Commands related to metadata pro formas"""
    ctx.context = ctx.parent.context

# proforma-specific options used in multiple commands
opt_required = create_option(
    '-req',
    '--required-field',
    help='Required field in this pro forma; users must populate this field in every upload. '
         'Multiple fields may be specified.',
    type=click.STRING,
    multiple=True)

opt_optional = create_option(
    '-opt',
    '--optional-field',
    help='Optional field in this pro forma; users may include this field in uploads. '
         'Multiple fields may be specified.',
    type=click.STRING,
    multiple=True)

@proforma.command('add', hidden=hide_admin_cmds())
@opt_abbrev()
@opt_name()
@opt_description(required=False)
@opt_required
@opt_optional
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
@opt_required
@opt_optional
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


@proforma.command('attach', hidden=hide_admin_cmds())
@click.argument('abbrev', type=click.STRING)
@create_option('-f',
              '--file-path',
              help='File that you may want to link.  '
                   'Only one xlsx filepath will be accepted',
              cls=MutuallyExclusiveOption,
              mutually_exclusive=["n_previous"])
@create_option('-n',
              '--n-previous',
              cls=MutuallyExclusiveOption,
              help="If pulling a file from a previous version, "
                   "of all versions that had a file attached, "
                   "how many steps back to pull from. 1 means "
                   "the first previous version that has a file "
                   "attachment. 2 means the second previous version "
                   "that as a file attachment, etc..",
              type=click.INT,
              mutually_exclusive=["file_path"])
def proforma_attach(abbrev: str,
                    file_path: str = None,
                    n_previous: int = None):
    """
    This command will attach a file or pull a existing file to latest ProForma Version

    Usage:

    austrakka proforma attach [ABBREV] ~~This will pull the file from the last proforma version

    austrakka proforma attach [ABBREV] -f [FILEPATH] ~~attaches given file

    austrakka proforma attach [ABBREV] -id [PROFORMA-VERSION-ID]
    ~~this pulls a file from specified id

    ABBREV should be the abbreviated name of the pro forma.
    """
    if file_path is None:
        pull_proforma(abbrev, n_previous)
    else:
        attach_proforma(abbrev, file_path)

@proforma.command('generate')
@click.argument('abbrev', type=click.STRING)
@create_option(
    '-r',
    '--restrict',
    type=click.STRING,
    multiple=True,
    nargs=2,
    help='Key-value pair; restrict the specified field to the specified '+
        'comma-separated subset of values. Multiple restrictions may be specifed')
@create_option(
    '--nndss/--no-nndss',
    type=bool,
    default=False,
    help='Include an NNDSS label column in the Data Dictionary',
)
@opt_project(
    required=False,
    help="Project to fill in on the Groups for Sharing tab",
)
@create_option(
    '-c',
    '--metadata-class',
    type=click.STRING,
    multiple=True,
    nargs=2,
    help='Key-value pair; add a metadata field class and assign it to the specified '+
        'comma-separated subset of fields',
)
def proforma_generate(abbrev: str, restrict, nndss, project, metadata_class):
    """
    Generate a draft XLSX pro forma template from the current specification.
    """
    generate_proforma(
        abbrev,
        restrict,
        nndss_column=nndss,
        project_abbrev=project,
        metadata_classes=metadata_class
        )

@proforma.command('list')
@table_format_option()
def proforma_list(out_format: str):
    """List metadata pro formas in AusTrakka"""
    list_proformas(out_format)


@proforma.command('show')
@click.argument('abbrev', type=click.STRING)
@table_format_option()
def proforma_show(abbrev: str, out_format: str):
    """
    Show pro forma fields.

    USAGE:
    austrakka proforma show [ABBREV]

    ABBREV should be the abbreviated name of the pro forma.
    Use `austrakka proforma list` for options.
    """
    show_proforma(abbrev, out_format)


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
@opt_group_name(var_name='group_names', multiple=True)
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
@opt_group_name(var_name='group_names', multiple=True)
def proforma_unshare(abbrev: str, group_names: List[str]):
    """
    UnShare a pro forma with one or more groups to prevent the proforma
    being returned in the `list` operation.

    USAGE:
    austrakka proforma unshare -g [GROUP NAME] [ABBREV]

    ABBREV should be the abbreviated name of the pro forma.
    """
    unshare_proforma(abbrev, group_names)


@proforma.command('list-groups')
@click.argument('abbrev', type=click.STRING)
@table_format_option()
def proforma_list_groups(abbrev: str, out_format: str):
    """
    List groups who have access to the given pro forma.

    USAGE:
    austrakka proforma listgroups [ABBREV]

    ABBREV should be the abbreviated name of the pro forma.
    """
    list_groups_proforma(abbrev, out_format)
