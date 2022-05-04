# pylint: disable=redefined-outer-name
from io import BufferedReader
import click

from austrakka.utils.options import opt_species
from .static import add_static
from ..analysis.opts import analysis


@click.group()
@click.pass_context
def static(ctx):
    '''Commands related to static analyses'''
    ctx.creds = ctx.parent.creds


@static.command('add')
@click.argument('csv', type=click.File('rb'))
@analysis
def static_add(csv: BufferedReader, analysis: int):
    '''Upload static analysis to AusTrakka'''
    add_static(csv, analysis)
