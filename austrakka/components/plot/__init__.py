# pylint: disable=expression-not-assigned,duplicate-code
from io import BufferedReader

import click

from austrakka.components.plot.funcs import add_plot, update_plot, disable_plot, enable_plot, \
    list_plot_types, list_plots
from austrakka.utils.output import table_format_option
from austrakka.utils.cmd_filter import hide_admin_cmds
from austrakka.utils.options import opt_abbrev, opt_plottype, opt_plotspec
from austrakka.utils.options import opt_description
from austrakka.utils.options import opt_is_active
from austrakka.utils.options import opt_project
from austrakka.utils.options import opt_name
from austrakka import __prog_name__ as PROG_NAME


@click.group()
@click.pass_context
def plot(ctx):
    '''Commands related to plots'''
    ctx.context = ctx.parent.context


@plot.command('list', help=f'List plots in {PROG_NAME}, by project')
@opt_project(required=True)
@table_format_option()
def plot_list(project: str, out_format: str):
    list_plots(project, out_format)


@plot.command('add', hidden=hide_admin_cmds(), help=f"Add plot to a project in {PROG_NAME}")
@opt_abbrev()
@opt_name()
@opt_description()
@opt_project()
@opt_plottype()
@opt_plotspec()
@opt_is_active()
def plot_add(
        abbrev: str,
        name: str,
        description: str,
        project: str,
        plottype: str,
        spec: BufferedReader,
        is_active: bool,
):
    add_plot(
        abbrev,
        name,
        description,
        project,
        plottype,
        spec,
        is_active,
    )


@plot.command('update', hidden=hide_admin_cmds(), help=f"Update a plot in {PROG_NAME}")
@click.argument('plot-abbrev', type=str)
@opt_name(required=False)
@opt_description(required=False)
@opt_project(required=False)
@opt_plottype(required=False)
@opt_plotspec()
@opt_is_active(is_update=True)
def plot_update(
        plot_abbrev: str,
        name: str,
        description: str,
        project: str,
        plottype: str,
        spec: BufferedReader,
        is_active: bool,
):
    update_plot(
        plot_abbrev,
        name,
        description,
        project,
        plottype,
        spec,
        is_active,
    )


@plot.command('disable', hidden=hide_admin_cmds())
@click.argument('plot-abbrev', type=click.STRING)
def plot_disable(plot_abbrev: str):
    """
    Disable a plot
    """
    disable_plot(plot_abbrev)


@plot.command('enable', hidden=hide_admin_cmds())
@click.argument('plot-abbrev', type=click.STRING)
def plot_enable(plot_abbrev: str):
    """
    Enable a plot
    """
    enable_plot(plot_abbrev)


@plot.command('types', help=f'List recognised plot types within {PROG_NAME}')
def plot_types():
    list_plot_types()
