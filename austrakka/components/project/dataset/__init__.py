import click
from austrakka.utils.options import opt_analysis_label, \
    opt_tracking_token, \
    opt_abbrev, opt_detailed, \
    opt_output_dir
from austrakka.components.project.dataset.funcs import add_dataset_blocking, \
    list_dataset_views, \
    download_dataset_view, active_dataset_entry_list_get
from austrakka.components.project.dataset.funcs import add_dataset, \
    track_dataset
from austrakka.utils.output import table_format_option


@click.group()
@click.pass_context
def dataset(ctx):
    """Commands to upload project datasets"""
    ctx.context = ctx.parent.context


@dataset.command('async-add')
@click.option('-fp',
              '--file-path',
              help='dataset csv file to upload to the project', )
@opt_analysis_label()
@opt_abbrev(help="Project Abbreviation")
def dataset_add(
        file_path: str,
        analysis_label: str,
        abbrev: str):
    """Upload a dataset file to the given project in AusTrakka."""
    add_dataset(file_path, analysis_label, abbrev)


@dataset.command('track-job')
@opt_abbrev(help="Project Abbreviation")
@opt_tracking_token()
@opt_detailed()
@table_format_option()
def dataset_track(
        abbrev: str,
        tracking_token: str,
        detailed: bool,
        out_format: str,
):
    """Check for a job states given a project in AusTrakka and a Tracking Token """
    track_dataset(abbrev, tracking_token, detailed, out_format)


@dataset.command('add')
@click.option('-fp',
              '--file-path',
              help='dataset csv file to upload to the project', )
@opt_analysis_label()
@opt_abbrev(help="Project Abbreviation")
@table_format_option()
def dataset_blocking_add(file_path: str,
                         analysis_label: str,
                         abbrev: str,
                         out_format: str,):
    """A blocking version of the dataset which uploads and polls the status of the job sent"""
    add_dataset_blocking(file_path, analysis_label, abbrev, out_format)


@dataset.command('list-views')
@opt_abbrev(help="Project Abbreviation")
@table_format_option()
def get_dataset_view_list(abbrev: str, out_format: str):
    """Get a list of views for a given project"""
    list_dataset_views(abbrev, out_format)


@dataset.command('get-view')
@click.option('-id',
              '--dataset-view-id',
              help='dataset view to get', )
@opt_abbrev(help="Project Abbreviation")
@opt_output_dir()
def get_dataset_view(output_dir: str,
                     dataset_view_id: str,
                     abbrev: str):
    """Get a dataset view for a given project"""
    download_dataset_view(output_dir, dataset_view_id, abbrev)


@dataset.command('active')
@opt_abbrev(help="Project Abbreviation")
@table_format_option()
def get_active_dataset_entry_list(abbrev: str, out_format: str):
    """Get a list of active datasets for a given project"""
    active_dataset_entry_list_get(abbrev, out_format)
