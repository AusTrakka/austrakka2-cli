import click

from austrakka.utils.options import opt_analysis_label, opt_tracking_token, opt_abbrev, opt_detailed
from austrakka.components.project.dataset.funcs import add_dataset, ack_dataset, track_dataset, add_dataset_blocking
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


@dataset.command('ack')
@opt_abbrev(help="Project Abbreviation")
@opt_tracking_token()
def dataset_ack(
        abbrev: str,
        tracking_token: str):
    """Acknowledge a dataset file to the given project in AusTrakka and a Tracking Token."""
    ack_dataset(abbrev, tracking_token)


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
    print(detailed)
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

    add_dataset_blocking(file_path, analysis_label, abbrev, out_format)

