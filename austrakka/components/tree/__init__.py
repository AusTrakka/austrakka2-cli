# pylint: disable=redefined-outer-name
from io import BufferedReader
import click

from .funcs import add_tree
from .funcs import list_trees
from .funcs import disable_tree
from .funcs import enable_tree
from ...utils.options import opt_analysis
from ...utils.options import opt_tree_id
from ...utils.output import table_format_option


@click.group()
@click.pass_context
def tree(ctx):
    '''Commands related to trees'''
    ctx.context = ctx.parent.context


@tree.command('add')
@click.argument('newick', type=click.File('rb'))
@opt_analysis()
def tree_add(newick: BufferedReader, analysis: str):
    '''Upload tree to AusTrakka'''
    add_tree(newick, analysis)


@tree.command('list')
@opt_analysis()
@table_format_option()
def tree_list(analysis: str, out_format: str):
    '''List trees in AusTrakka'''
    list_trees(out_format, analysis)


@tree.command('disable')
@opt_tree_id()
def tree_disable(tree_id: int):
    '''Disable a tree'''
    disable_tree(tree_id)


@tree.command('enable')
@opt_tree_id()
def tree_enable(tree_id: int):
    '''Enable a tree'''
    enable_tree(tree_id)
