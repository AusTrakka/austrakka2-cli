from typing import List

import click

from austrakka.utils.output import table_format_option
from austrakka.utils.cmd_filter import hide_admin_cmds
from austrakka.utils.options import opt_owner_group_roles
from austrakka.utils.options import opt_user_object_id
from austrakka.utils.options import opt_organisation
from .funcs import list_users
from .funcs import add_user
from .funcs import update_user


@click.group()
@click.pass_context
def user(ctx):
    '''Commands related to users'''
    ctx.creds = ctx.parent.creds


@user.command('list')
@table_format_option()
def user_list(out_format: str):
    '''List users in AusTrakka'''
    list_users(out_format)


@user.command('add', hidden=hide_admin_cmds())
@opt_user_object_id()
@opt_organisation()
@opt_owner_group_roles(required=False)
def user_add(
    user_id: str,
    org: str,
    owner_group_roles: List[str],
):
    """Add users in AusTrakka"""
    add_user(user_id, org, owner_group_roles)


@user.command('update', hidden=hide_admin_cmds())
@click.argument('user-id', type=int)
@opt_organisation(required=False)
@opt_owner_group_roles(required=False)
def user_update(
    user_id: int,
    org: str,
    owner_group_roles: List[str],
):
    """Add users in AusTrakka"""
    update_user(user_id, org, owner_group_roles)
