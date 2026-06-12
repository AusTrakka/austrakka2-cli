from typing import Optional

import click

from austrakka.utils.output import table_format_option
from austrakka.utils.output import FORMATS

from .funcs import get_view, \
    download_view

@click.group()
@click.pass_context
def metadata(ctx):
    """Commands to query for metadata views for a project, including commands for setting how 
    the views are generated. This sub command is predominantly used for fetching metadata 
    that was uploaded and shared with the project, as well as project analysis metadata 
    that was uploaded by a project analyst. Data from both sources are merged to create a unified
    view which is accessible to project members. 
    """
    ctx.context = ctx.parent.context


@metadata.command('get')
@click.argument('project-abbrev', type=str)
@table_format_option()
def get_dataset_view(project_abbrev: str, out_format: str):
    """Get view information for a given project."""
    get_view(project_abbrev, out_format)

@metadata.command('download')
@click.argument('project-abbrev', type=str)
@table_format_option(FORMATS.CSV)
def download_dataset_view(
        project_abbrev: str,
        out_format: str,
):
    """Download sample metadata for the project."""
    download_view(project_abbrev, out_format)
