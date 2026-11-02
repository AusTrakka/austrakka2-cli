import click
from trakka.utils.options import opt_analysis_label
from trakka.components.project.dataset.funcs import add_dataset, \
    list_dataset, disable_dataset
from trakka.utils.output import table_format_option


@click.group()
@click.pass_context
def dataset(ctx):
    """Commands to manage project datasets"""
    ctx.context = ctx.parent.context

@dataset.command('add')
@click.argument('project-abbrev', type=str)
@click.option('-fp',
              '--file-path',
              help='dataset csv file to upload to the project', )
@opt_analysis_label()
def dataset_add(project_abbrev: str,
                         file_path: str,
                         analysis_label: str,
):
    """Upload a dataset"""
    add_dataset(file_path, analysis_label, project_abbrev)


@dataset.command('list')
@click.argument('project-abbrev', type=str)
@table_format_option()
def dataset_list(project_abbrev: str, out_format: str):
    """Get a list of active datasets for a given project"""
    list_dataset(project_abbrev, out_format)


@dataset.command('disable')
@click.option('-id',
              '--dataset-id',
              help='dataset to disable', )
@click.argument('project-abbrev', type=str)
def dataset_disable(project_abbrev: str, dataset_id: int):
    """Disable a dataset for a given project"""
    disable_dataset(project_abbrev, dataset_id)
