# pylint: disable=redefined-outer-name
from io import BufferedReader

import click

from austrakka.utils.options import opt_analysis
from .static import add_static


@click.group()
@click.pass_context
def static(ctx):
    '''Commands related to static analyses'''
    ctx.creds = ctx.parent.creds


@static.command('add')
@click.argument('csv', type=click.File('rb'))
@opt_analysis
def static_add(csv: BufferedReader, analysis: int):
    '''Upload static analysis to AusTrakka'''
    add_static(csv, analysis)
