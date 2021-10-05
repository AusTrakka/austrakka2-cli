from io import BufferedReader
import click

from .submission import add_submission


@click.group()
@click.pass_context
def submission(ctx):
    '''Commands related to submissions'''
    ctx.creds = ctx.parent.creds


@submission.command('add')
@click.argument('file', type=click.File('rb'))
@click.option(
    '-s',
    '--species',
    required=True,
    help='Species ID',
    type=click.INT
)
def submission_add(file: BufferedReader, species: int):
    '''Upload submission to AusTrakka'''
    add_submission(file, species)
