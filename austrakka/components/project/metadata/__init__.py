from typing import Optional

import click

from austrakka.utils.output import table_format_option
from austrakka.utils.output import FORMATS
from austrakka.utils.options import opt_merge_algorithm
from austrakka.utils.options import opt_view_id

from .funcs import list_dataset_views, \
    download_dataset_view

@click.group()
@click.pass_context
def metadata(ctx):
    """Commands to query for metadata views for a project, including commands for setting how 
    the views are generated. This sub command is predominantly used for fetching metadata 
    that was uploaded and shared with the project, as well as project analysis metadata 
    that was uploaded by a project analyst. Data from both sources are merged to create 
    one or more unified views which are accessible to project members. 

    All views have the same number of sample rows but differ in the number of fields. The
    base view contains all fields which are accessible by the project. All other views are
    subsets of the base."""
    ctx.context = ctx.parent.context


@metadata.command('list')
@click.argument('project-abbrev', type=str)
@table_format_option()
def get_dataset_view_list(project_abbrev: str, out_format: str):
    """Get a list of metadata views for a given project."""
    list_dataset_views(project_abbrev, out_format)

@metadata.command('get')
@opt_view_id()
@click.argument('project-abbrev', type=str)
@table_format_option(FORMATS.CSV)
def get_dataset_view(
        project_abbrev: str,
        view_id: Optional[str],
        out_format: str,
):
    """Get a specific metadata view. By default, the full metadata view is returned."""
    download_dataset_view(view_id, project_abbrev, out_format)
