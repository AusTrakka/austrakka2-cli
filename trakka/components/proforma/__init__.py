from typing import List


from trakka.components.proforma.org import org
from trakka.components.proforma.project import project
from trakka.components.proforma.field import field
from trakka.utils.output import object_format_option, table_format_option
from trakka.utils.cmd_filter import hide_admin_cmds
from trakka.utils.privilege import PROFORMA_RESOURCE
from trakka.components.privilege import privilege_subcommands
from trakka.components.log import log_subcommands
from .funcs import \
    add_proforma, \
    update_proforma, \
    add_version_proforma, \
    list_proformas, \
    show_proforma, \
    disable_proforma, \
    enable_proforma

from ...utils.options import *


@click.group()
@click.pass_context
def proforma(ctx):
    """Commands related to metadata proformas"""
    ctx.context = ctx.parent.context

proforma.add_command(privilege_subcommands(PROFORMA_RESOURCE))
proforma.add_command(log_subcommands(PROFORMA_RESOURCE))
proforma.add_command(org)
proforma.add_command(project)
proforma.add_command(field)

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
        help="""
            Add a new proforma.
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
@click.option(
        '--force',
        type=bool,
        is_flag=True,
        default=False,
        help="[deprecated] Creates a new version even if the columns are the same"
)
@click.argument('proforma-abbrev', type=click.STRING)
def proforma_add_version(
        proforma_abbrev: str,
        required_field: List[str],
        optional_field: List[str],
        remove_field: List[str],
        inherit: bool,
        force: bool,
):
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
        inherit,
        force,
    )


@proforma.command('list', help='List metadata proformas')
@opt_view_type()
@table_format_option()
def proforma_list(view_type: str, out_format: str):
    list_proformas(view_type, out_format)


@proforma.command('show')
@click.argument('proforma-abbrev', type=click.STRING)
@object_format_option()
def proforma_show(proforma_abbrev: str, out_format: str):
    """
    Show proforma details

    See `trakka proforma list` for available pro formas.
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
