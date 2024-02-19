import click

from austrakka.utils.output import table_format_option
from austrakka.utils.options import \
    opt_merge_algorithm, \
    opt_output_dir

from .funcs import list_dataset_views, \
    download_dataset_view, \
    set_merge_algorithm_project


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
@click.argument('abbrev', type=str)
@table_format_option()
def get_dataset_view_list(abbrev: str, out_format: str):
    """Get a list of metadata views for a given project."""
    list_dataset_views(abbrev, out_format)


@metadata.command('get')
@click.option('-id',
              '--view-id',
              help='Project metadata view to get', )
@click.argument('abbrev', type=str)
@opt_output_dir()
def get_dataset_view(abbrev: str,
                     output_dir: str,
                     view_id: str,):
    """Get a specific metadata view."""
    download_dataset_view(output_dir, view_id, abbrev)


@metadata.command('set-merge')
@click.argument('abbrev', type=str)
@opt_merge_algorithm()
def project_set_merge_algo(abbrev: str, merge_algorithm):
    """
    Set merge algorithm to use when generating metadata views.
    """
    set_merge_algorithm_project(abbrev, merge_algorithm)
