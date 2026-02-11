# pylint: disable=expression-not-assigned,duplicate-code
from io import BufferedReader
import click

from austrakka.utils.output import table_format_option
from austrakka.components.tree.version import version
from austrakka.components.tree.funcs import list_trees, disable_tree, enable_tree
from austrakka.components.tree.funcs import add_tree
from austrakka.components.tree.funcs import update_tree
from austrakka.utils.cmd_filter import show_admin_cmds
from austrakka.utils.cmd_filter import hide_admin_cmds
from austrakka.utils.options import opt_abbrev, opt_file, opt_show_disabled
from austrakka.utils.options import opt_name
from austrakka.utils.options import opt_description
from austrakka.utils.options import opt_is_active
from austrakka.utils.options import opt_project


@click.group()
@click.pass_context
def tree(ctx):
    '''Commands related to trees'''
    ctx.context = ctx.parent.context


tree.add_command(version) if show_admin_cmds() else None


@tree.command('list')
@opt_project(required=True)
@opt_show_disabled()
@table_format_option()
def tree_list(project: str, show_disabled: bool, out_format: str):
    '''List trees in AusTrakka'''
    list_trees(project, show_disabled, out_format)


@tree.command('add')
@opt_abbrev()
@opt_name(help='Tree Name')
@opt_description()
@opt_project()
@opt_is_active()
@opt_file(help='Newick File')
def tree_add(
        abbrev: str,
        name: str,
        description: str,
        project: str,
        is_active: bool,
        file: BufferedReader,
):
    """Add a new named tree to a project. If a newick file is supplied, it
    will be uploaded to this tree entry, otherwise the tree entry will appear
    in the project with no tree versions until one is added. To add a newick
    file to an existing named tree, use the tree version add command."""
    add_tree(
        abbrev,
        name,
        description,
        project,
        is_active,
        file,
    )


@tree.command('update')
@click.argument('tree-abbrev', type=str)
@opt_name(help='Tree Name', required=False)
@opt_description(required=False)
@opt_project(required=False)
@opt_is_active(is_update=True)
def tree_update(
        tree_abbrev: str,
        name: str,
        description: str,
        project: str,
        is_active: bool,
):
    """Update the properties of a named tree. This does not upload a newick
    file and does not create a new version of the specified tree."""
    update_tree(
        tree_abbrev,
        name,
        description,
        project,
        is_active,
    )


@tree.command('disable', hidden=hide_admin_cmds())
@click.argument('tree-abbrev', type=str)
def tree_disable(tree_abbrev: str):
    """Disable a named tree and all its versions."""
    disable_tree(tree_abbrev)


@tree.command('enable', hidden=hide_admin_cmds())
@click.argument('tree-abbrev', type=str)
def tree_enable(tree_abbrev: str):
    """Re-enable a named tree and all its versions"""
    enable_tree(tree_abbrev)
