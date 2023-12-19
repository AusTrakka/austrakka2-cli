import click

from austrakka.components.project.setup.funcs import add_field_project, set_merge_algorithm_project, \
    add_provision_project
from austrakka.utils.cmd_filter import hide_admin_cmds
from austrakka.utils.options import opt_field_name, MutuallyExclusiveOption, opt_project, opt_merge_algorithm, \
    opt_field_and_source, opt_abbrev


# pylint: disable=duplicate-code
@click.group()
@click.pass_context
def setup(ctx):
    """Commands to upload project datasets"""
    ctx.context = ctx.parent.context


@setup.command('add-fields', hidden=hide_admin_cmds())
@opt_abbrev()
@opt_field_and_source()
def project_add_field(abbrev, field_source):
    '''
    add fields for a given project.
    '''
    add_field_project(abbrev, field_source)


@setup.command('set-merge')
@opt_abbrev()
@opt_merge_algorithm()
def project_set_merge_algo(abbrev, merge_algorithm):
    """
    set merge algorithm for a given project
    """
    set_merge_algorithm_project(abbrev, merge_algorithm)


@setup.command('add-provision')
@opt_abbrev()
@opt_field_name()
def project_add_provision(abbrev, field_names):
    """This will add a project provision"""
    add_provision_project(abbrev, field_names)
