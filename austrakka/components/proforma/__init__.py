from typing import List


from austrakka.utils.output import table_format_option
from austrakka.utils.cmd_filter import hide_admin_cmds
from austrakka.utils.privilege import PROFORMA_RESOURCE
from austrakka.utils.subcommands.log import log_subcommands
from .funcs import \
    add_proforma, \
    update_proforma, \
    add_version_proforma, \
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
    """Commands related to metadata proformas"""
    ctx.context = ctx.parent.context

proforma.add_command(log_subcommands(PROFORMA_RESOURCE))

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

opt_remove = create_option(
    '-rm',
    '--remove-field',
    help='Field to remove from the pro forma. Multiple fields may be specified.',
    type=click.STRING,
    multiple=True
)

def opt_inherit(**attrs: t.Any):
    defaults = {
        'is_flag': True,
        'default': False,
        'help': 'Inherit fields from previous version',
    }
    return create_option(
        '--inherit',
        **{**defaults, **attrs}
    )


@proforma.command(
        'add', 
        hidden=hide_admin_cmds(),
        help=f"""
            Add a new proforma to {PROG_NAME}.
            This adds a validation spec which may be selected to upload data. 
            This will add a new proforma with a new abbreviation, not a new version of an existing proforma.
            This command does not add the Excel proforma template document; 
            that should be added wih the 'attach' command.
        """
)
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
    add_proforma(
        abbrev,
        name,
        description,
        required_field,
        optional_field)

@proforma.command('update', hidden=hide_admin_cmds())
@opt_name(required=False)
@opt_description(required=False)
@click.argument('proforma-abbrev', type=click.STRING)
def proforma_update(
        proforma_abbrev: str,
        name: str,
        description: str):
    """
    Update a pro forma's Name or Description
    """
    update_proforma(
        proforma_abbrev,
        name,
        description)


@proforma.command('add-version', hidden=hide_admin_cmds())
@opt_required
@opt_optional
@opt_remove
@opt_inherit()
@click.argument('proforma-abbrev', type=click.STRING)
def proforma_add_version(
        proforma_abbrev: str,
        required_field: List[str],
        optional_field: List[str],
        remove_field: List[str],
        inherit: bool):
    """
    Add a proforma version with a new set of fields.
    The fields specified by -req and -opt will fully replace the fields in the current version.
    Any fields in the current version but not listed in the update will be removed.
    """
    add_version_proforma(
        proforma_abbrev,
        required_field,
        optional_field,
        remove_field,
        inherit)


@proforma.command(
        'attach', 
        hidden=hide_admin_cmds(),
        help=f"""
            Attach a new or existing file to the latest version of the specified proforma.

            Usage:

            {PROG_NAME.lower()} proforma attach [PROFORMA_ABBREV] 
            ~~This will pull the most recent existing file from a previous proforma version

            {PROG_NAME.lower()} proforma attach [PROFORMA_ABBREV] -f [FILEPATH] ~~uploads and attaches a new file

            {PROG_NAME.lower()} proforma attach [PROFORMA_ABBREV] -id [PROFORMA-VERSION-ID]
            ~~This will pull an existing file from a previous proforma version
        """
)
@click.argument('proforma-abbrev', type=click.STRING)
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
def proforma_attach(proforma_abbrev: str,
                    file_path: str = None,
                    n_previous: int = None):
    if file_path is None:
        pull_proforma(proforma_abbrev, n_previous)
    else:
        attach_proforma(proforma_abbrev, file_path)

@proforma.command('generate')
@click.argument('proforma-abbrev', type=click.STRING)
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
@create_option(
    '-c',
    '--metadata-class',
    type=click.STRING,
    multiple=True,
    nargs=2,
    help='Key-value pair; add a metadata field class and assign it to the specified '+
        'comma-separated subset of fields',
)
def proforma_generate(proforma_abbrev: str, restrict, nndss, metadata_class):
    """
    Generate a draft XLSX pro forma template from the current specification.
    """
    generate_proforma(
        proforma_abbrev,
        restrict,
        nndss_column=nndss,
        metadata_classes=metadata_class
        )

@proforma.command('list', help=f'List metadata proformas in {PROG_NAME}')
@opt_view_type()
@table_format_option()
def proforma_list(view_type: str, out_format: str):
    list_proformas(view_type, out_format)


@proforma.command('show')
@click.argument('proforma-abbrev', type=click.STRING)
@table_format_option()
def proforma_show(proforma_abbrev: str, out_format: str):
    """
    Show pro forma fields.

    See `austrakka proforma list` for available pro formas.
    """
    show_proforma(proforma_abbrev, out_format)


@proforma.command('disable', hidden=hide_admin_cmds())
@click.argument('proforma-abbrev', type=click.STRING)
# Consider option instead: @opt_abbrev("Abbreviated name of the pro forma")
def proforma_disable(proforma_abbrev: str):
    """
    Disable a proforma.
    """
    disable_proforma(proforma_abbrev)


@proforma.command('enable', hidden=hide_admin_cmds())
@click.argument('proforma-abbrev', type=click.STRING)
# Consider option instead: @opt_abbrev("Abbreviated name of the pro forma")
def proforma_enable(proforma_abbrev: str):
    """
    Re-enable a proforma.
    """
    enable_proforma(proforma_abbrev)


@proforma.command('share', hidden=hide_admin_cmds())
@click.argument('proforma-abbrev', type=click.STRING)
@opt_group_name(var_name='group_names', multiple=True)
def proforma_share(proforma_abbrev: str, group_names: List[str]):
    """
    Share a proforma with one or more groups, which may be project groups. 
    The proforma will be visible and useable by Uploaders in these groups.
    """
    share_proforma(proforma_abbrev, group_names)


@proforma.command('unshare', hidden=hide_admin_cmds())
@click.argument('proforma-abbrev', type=click.STRING)
@opt_group_name(var_name='group_names', multiple=True)
def proforma_unshare(proforma_abbrev: str, group_names: List[str]):
    """
    Unshare a proforma with one or more groups.
    """
    unshare_proforma(proforma_abbrev, group_names)


@proforma.command('list-groups')
@click.argument('proforma-abbrev', type=click.STRING)
@table_format_option()
def proforma_list_groups(proforma_abbrev: str, out_format: str):
    """
    List groups which have access to the given proforma.
    """
    list_groups_proforma(proforma_abbrev, out_format)
