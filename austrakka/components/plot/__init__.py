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


@click.group()
@click.pass_context
def plot(ctx):
    '''Commands related to plots'''
    ctx.context = ctx.parent.context


@plot.command('list')
@opt_project(required=True)
@table_format_option()
def plot_list(project: str, out_format: str):
    '''List plots in AusTrakka, by project'''
    list_plots(project, out_format)


@plot.command('add', hidden=hide_admin_cmds())
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
    """Add plot to a project in AusTrakka"""
    add_plot(
        abbrev,
        name,
        description,
        project,
        plottype,
        spec,
        is_active,
    )


@plot.command('update', hidden=hide_admin_cmds())
@click.argument('abbrev', type=str)
@opt_name(required=False)
@opt_description(required=False)
@opt_project(required=False)
@opt_plottype(required=False)
@opt_plotspec()
@opt_is_active(is_update=True)
def plot_update(
        abbrev: str,
        name: str,
        description: str,
        project: str,
        plottype: str,
        spec: BufferedReader,
        is_active: bool,
):
    """Update a plot in AusTrakka"""
    update_plot(
        abbrev,
        name,
        description,
        project,
        plottype,
        spec,
        is_active,
    )


@plot.command('disable', hidden=hide_admin_cmds())
@click.argument('abbrev', type=click.STRING)
def plot_disable(abbrev: str):
    """
    Disable a plot

    USAGE:
    austrakka plot disable [ABBREV]

    ABBREV should be the abbreviated name of the pro forma.
    """
    disable_plot(abbrev)


@plot.command('enable', hidden=hide_admin_cmds())
@click.argument('abbrev', type=click.STRING)
def plot_enable(abbrev: str):
    """
    Enable a plot

    USAGE:
    austrakka plot enable [ABBREV]

    ABBREV should be the abbreviated name of the pro forma.
    """
    enable_plot(abbrev)


@plot.command('types')
def plot_types():
    """
    List recognised plot types within AusTrakka
    """
    list_plot_types()
