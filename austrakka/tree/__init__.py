from io import BufferedReader
import click

from .tree import add_tree


@click.group()
@click.pass_context
def tree(ctx):
    '''Commands related to trees'''
    ctx.creds = ctx.parent.creds


@tree.command('add')
@click.argument('newick', type=click.File('rb'))
@click.option(
    '-a',
    '--analysis',
    required=True,
    help='Analysis ID',
    type=click.INT
)
def tree_list(newick: BufferedReader, analysis: int):
    '''Upload tree to AusTrakka'''
    add_tree(newick, analysis)
