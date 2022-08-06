from typing import List
import click

from austrakka.utils.output import table_format_option
from austrakka.utils.cmd_filter import hide_admin_cmds
from .funcs import \
    add_group, \
    update_group, \
    list_group

from ...utils.options import *


@click.group()
@click.pass_context
def group(ctx):
    """Commands related to groups"""
    ctx.creds = ctx.parent.creds


@group.command('add', hidden=hide_admin_cmds())
@opt_name()
@opt_organisation(required=False)
def group_add(
        name: str,
        org):
    """
    Add a new group to the given organisation.
    """
    add_group(name, org)


@group.command('update', hidden=hide_admin_cmds())
@opt_name()
@opt_newname(required=False)
@opt_organisation(required=False)
def group_update(
        name: str,
        newname: str,
        org: str):
    """
    Update a group name or organisation.
    """
    update_group(
        name,
        newname,
        org)


@group.command('list')
@table_format_option()
def group_list(table_format: str):
    """List all known groups in AusTrakka"""
    list_group(table_format)
