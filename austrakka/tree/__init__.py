# pylint: disable=redefined-outer-name
from io import BufferedReader
import click

from .funcs import add_tree
from ..species.opts import species
from ..analysis.opts import analysis


@click.group()
@click.pass_context
def tree(ctx):
    '''Commands related to trees'''
    ctx.creds = ctx.parent.creds


@tree.command('add')
@click.argument('newick', type=click.File('rb'))
@analysis
@species
def tree_add(newick: BufferedReader, analysis: int, species: int):
    '''Upload tree to AusTrakka'''
    add_tree(newick, analysis, species)
