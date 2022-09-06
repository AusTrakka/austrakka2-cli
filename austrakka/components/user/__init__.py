from typing import List

import click

from austrakka.utils.cmd_filter import hide_admin_cmds
from austrakka.utils.options import opt_owner_group_roles
from austrakka.utils.options import opt_user_email
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
def user_list():
    '''List users in AusTrakka'''
    list_users()


@user.command('add', hidden=hide_admin_cmds())
@opt_user_email()
@opt_organisation()
@opt_owner_group_roles(required=False)
def user_add(
    email: str,
    org: str,
    owner_group_roles: List[str],
):
    """Add users in AusTrakka"""
    add_user(email, org, owner_group_roles)


@user.command('update', hidden=hide_admin_cmds())
@click.argument('email', type=str)
@opt_organisation(required=False)
@opt_owner_group_roles(required=False)
def user_update(
    email: str,
    org: str,
    owner_group_roles: List[str],
):
    """Add users in AusTrakka"""
    update_user(email, org, owner_group_roles)
