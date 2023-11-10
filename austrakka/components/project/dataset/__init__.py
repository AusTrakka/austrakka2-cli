import click

from austrakka.utils.options import opt_analysis_label
from austrakka.utils.options import opt_abbrev
from austrakka.components.project.dataset.funcs import add_dataset


@click.group()
@click.pass_context
def dataset(ctx):
    """Commands to upload project datasets"""
    ctx.context = ctx.parent.context


@dataset.command('async-add')
@click.option('-f',
              '--file-path',
              help='dataset csv file to upload to the project',)
@opt_analysis_label()
@opt_abbrev(help="Project Abbreviation")
def dataset_add(
        file_path: str,
        analysis_label: str,
        abbrev: str):
    """Upload a dataset file to the given project in AusTrakka."""
    add_dataset(file_path, analysis_label, abbrev)
