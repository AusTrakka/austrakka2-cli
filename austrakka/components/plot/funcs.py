from io import BufferedReader

from loguru import logger

from austrakka.utils.api import api_post, api_patch, api_get, api_put
from austrakka.utils.helpers.output import call_get_and_print
from austrakka.utils.helpers.project import get_project_by_abbrev
from austrakka.utils.helpers.plots import get_plot_by_abbrev
from austrakka.utils.misc import logger_wraps
from austrakka.utils.paths import PLOT_PATH


@logger_wraps()
def list_plots(
        project_abbrev: str,
        out_format: str
):
    # get project ID
    project = get_project_by_abbrev(project_abbrev)
    call_get_and_print(
        f'{PLOT_PATH}/project/{project["projectId"]}',
        out_format)


@logger_wraps()
def show_plot():
    pass


@logger_wraps()
def add_plot(
        abbrev: str,
        name: str,
        description: str,
        project: str,
        plottype: str,
        spec: BufferedReader,
        is_active: bool,
):
    if spec is not None:
        spec_string = spec.read()
    else:
        spec_string = None
    api_post(
        path=PLOT_PATH,
        data={
            'name': name,
            'abbreviation': abbrev,
            'description': description,
            'projectAbbreviation': project,
            'plotTypeName': plottype,
            'spec': spec_string,
            'isActive': is_active,
        }
    )


@logger_wraps()
def update_plot(
        abbrev: str,
        name: str,
        description: str,
        project: str,
        plot_type: str,
        spec: str,
        is_active: bool,
):
    if spec is not None:
        spec_string = spec.read()
    else:
        spec_string = None
            
    plot = get_plot_by_abbrev(abbrev)
    plot_put = {
        prop: plot[prop] for prop in [
            'abbreviation',
            'name',
            'description',
            'spec',
            'projectAbbreviation',
            'isActive']}
    plot_put['plotTypeName'] = plot['plotType']

    if name is not None:
        plot_put['name'] = name
    if description is not None:
        plot_put['description'] = description
    if project is not None:
        plot_put['project'] = project
    if is_active is not None:
        plot_put['isActive'] = is_active
    if plot_type is not None:
        plot_put['plotType'] = plot_type
    if spec_string is not None:
        plot_put['spec'] = spec_string

    api_put(
        path=f'{PLOT_PATH}/{abbrev}',
        data=plot_put
    )


@logger_wraps()
def disable_plot(abbrev: str):
    logger.info(f'Disabling pro forma: {abbrev}..')

    api_patch(
        path=f'{PLOT_PATH}/{abbrev}/disable',
    )

    logger.info('Done.')


@logger_wraps()
def enable_plot(abbrev: str):
    logger.info(f'Enabling pro forma: {abbrev}..')

    api_patch(
        path=f'{PLOT_PATH}/{abbrev}/enable',
    )

    logger.info('Done.')


@logger_wraps()
def list_plot_types():
    response = api_get(
        path=f'{PLOT_PATH}/plottypes'
    )
    for plottype in response['data']:
        # pylint: disable=print-function
        print(plottype['name'])
