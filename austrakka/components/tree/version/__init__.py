# pylint: disable=redefined-outer-name
from io import BufferedReader
import click

from .funcs import add_tree_version
from .funcs import list_tree_versions
from .funcs import disable_tree_version
from .funcs import enable_tree_version
from ....utils.options import opt_tree
from ....utils.options import opt_tree_version_id
from ....utils.output import table_format_option


@click.group()
@click.pass_context
def version(ctx):
    '''Commands related to tree versions'''
    ctx.context = ctx.parent.context


@version.command('add')
@click.argument('newick', type=click.File('rb'))
@opt_tree()
def tree_add(newick: BufferedReader, tree: str):
    '''Upload a new version of the specified tree'''
    add_tree_version(newick, tree)


@version.command('list')
@opt_tree()
@table_format_option()
def tree_list(tree: str, out_format: str):
    '''List all uploaded versions of a specified tree'''
    list_tree_versions(out_format, tree)


@version.command('disable')
@opt_tree_version_id()
def tree_disable(tree_version_id: int):
    '''Disable a tree version'''
    disable_tree_version(tree_version_id)


@version.command('enable')
@opt_tree_version_id()
def tree_enable(tree_version_id: int):
    '''Enable a tree version'''
    enable_tree_version(tree_version_id)
