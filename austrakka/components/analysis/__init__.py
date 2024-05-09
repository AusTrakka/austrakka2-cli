# pylint: disable=expression-not-assigned,duplicate-code
import click

from austrakka.utils.output import table_format_option
from austrakka.components.analysis.definition import definition
from austrakka.components.analysis.funcs import list_analyses, disable_analysis, enable_analysis
from austrakka.components.analysis.funcs import add_analysis
from austrakka.components.analysis.funcs import update_analysis
from austrakka.utils.cmd_filter import show_admin_cmds
from austrakka.utils.cmd_filter import hide_admin_cmds
from austrakka.utils.options import opt_abbrev, opt_show_disabled
from austrakka.utils.options import opt_name
from austrakka.utils.options import opt_description
from austrakka.utils.options import opt_is_active
from austrakka.utils.options import opt_project
from austrakka.utils.options import opt_definition
from austrakka.utils.options import opt_filter_string


@click.group()
@click.pass_context
def analysis(ctx):
    '''Commands related to analyses'''
    ctx.context = ctx.parent.context


analysis.add_command(definition) if show_admin_cmds() else None


@analysis.command('list')
@opt_project(required=True)
@opt_show_disabled()
@table_format_option()
def analysis_list(project: str, show_disabled: bool, out_format: str):
    '''List analyses in AusTrakka'''
    list_analyses(project, show_disabled, out_format)


@analysis.command('add')
@opt_abbrev()
@opt_name(help='Analysis Name')
@opt_description()
@opt_project()
@opt_definition(var_name='definition_abbrev')
@opt_filter_string(required=False)
@opt_is_active()
def analysis_add(
        abbrev: str,
        name: str,
        description: str,
        project: str,
        definition_abbrev: str,
        filter_str: str,
        is_active: bool,
):
    """Add analysis in AusTrakka"""
    add_analysis(
        abbrev,
        name,
        description,
        project,
        definition_abbrev,
        filter_str,
        is_active,
    )


@analysis.command('update')
@click.argument('abbrev', type=str)
@opt_name(help='Analysis Name', required=False)
@opt_description(required=False)
@opt_project(required=False)
@opt_definition(var_name='definition_abbrev', required=False)
@opt_filter_string(required=False)
@opt_is_active(is_update=True)
def analysis_update(
        abbrev: str,
        name: str,
        description: str,
        project: str,
        definition_abbrev: str,
        filter_str: str,
        is_active: bool,
):
    """Update analysis in AusTrakka"""
    update_analysis(
        abbrev,
        name,
        description,
        project,
        definition_abbrev,
        filter_str,
        is_active,
    )


@analysis.command('disable', hidden=hide_admin_cmds())
@click.argument('abbrev', type=str)
def analysis_disable(abbrev: str):
    """Disable analysis in AusTrakka"""
    disable_analysis(abbrev)


@analysis.command('enable', hidden=hide_admin_cmds())
@click.argument('abbrev', type=str)
def analysis_enable(abbrev: str):
    """Enable analysis in AusTrakka"""
    enable_analysis(abbrev)
