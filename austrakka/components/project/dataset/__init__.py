import click
from austrakka.utils.options import opt_analysis_label, \
    opt_tracking_token, \
    opt_detailed
from austrakka.components.project.dataset.funcs import add_dataset_blocking, \
    active_dataset_entry_list_get, disable_dataset
from austrakka.components.project.dataset.funcs import add_dataset, \
    track_dataset
from austrakka.utils.output import table_format_option
from austrakka import __prog_name__ as PROG_NAME


@click.group()
@click.pass_context
def dataset(ctx):
    """Commands to manage project datasets"""
    ctx.context = ctx.parent.context


@dataset.command(
        'async-add',
        help=f'Upload a dataset file to the given project in {PROG_NAME}.',
)
@click.argument('project-abbrev', type=str)
@click.option('-fp',
              '--file-path',
              help='dataset csv file to upload to the project', )
@opt_analysis_label()
def dataset_add(
        project_abbrev: str,
        file_path: str,
        analysis_label: str):
    add_dataset(file_path, analysis_label, project_abbrev)


@dataset.command(
        'track-upload',
        help=f'Check for a job states given a project in {PROG_NAME} and a Tracking Token',
)
@click.argument('project-abbrev', type=str)
@opt_tracking_token()
@opt_detailed()
@table_format_option()
def dataset_track(
        project_abbrev: str,
        tracking_token: str,
        detailed: bool,
        out_format: str,
):
    track_dataset(project_abbrev, tracking_token, detailed, out_format)


@dataset.command('add')
@click.argument('project-abbrev', type=str)
@click.option('-fp',
              '--file-path',
              help='dataset csv file to upload to the project', )
@opt_analysis_label()
@table_format_option()
def dataset_blocking_add(project_abbrev: str,
                         file_path: str,
                         analysis_label: str,
                         out_format: str,):
    """A blocking version of the dataset which uploads and polls the status of the job sent"""
    add_dataset_blocking(file_path, analysis_label, project_abbrev, out_format)


@dataset.command('list')
@click.argument('project-abbrev', type=str)
@table_format_option()
def get_active_dataset_entry_list(project_abbrev: str, out_format: str):
    """Get a list of active datasets for a given project"""
    active_dataset_entry_list_get(project_abbrev, out_format)


@dataset.command('disable')
@click.option('-id',
              '--dataset-id',
              help='dataset to disable', )
@click.argument('project-abbrev', type=str)
def project_dataset_disable(project_abbrev: str, dataset_id: int):
    """Disable a dataset for a given project"""
    disable_dataset(project_abbrev, dataset_id)
