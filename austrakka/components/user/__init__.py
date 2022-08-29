from typing import List

import click

from austrakka.utils.output import table_format_option
from austrakka.utils.cmd_filter import hide_admin_cmds
from austrakka.utils.options import opt_roles
from austrakka.utils.options import opt_user_email
from austrakka.utils.options import opt_organisation
from austrakka.utils.options import opt_is_active, opt_is_contributor, opt_is_owner
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
def user_list(table_format: str):
    '''List users in AusTrakka'''
    list_users(table_format)


@user.command('add', hidden=hide_admin_cmds())
@opt_user_email()
@opt_organisation()
@opt_roles()
@opt_is_active()
@opt_is_owner()
@opt_is_contributor()
def user_add(
    email: str,
    org: str,
    role: List[str],
    is_active: bool,
    is_owner: bool,
    is_contributor: bool
):
    """Add users in AusTrakka"""
    add_user(email, org, role, is_active, is_owner, is_contributor)


@user.command('update', hidden=hide_admin_cmds())
@click.argument('email', type=str)
@opt_organisation(required=False)
@opt_roles(required=False)
@opt_is_active(is_update=True)
@opt_is_owner(is_update=True)
@opt_is_contributor(is_update=True)
def user_update(
    email: str,
    org: str,
    role: List[str],
    is_active: bool,
    is_owner: bool,
    is_contributor: bool
):
    """Add users in AusTrakka"""
    update_user(email, org, role, is_active, is_owner, is_contributor)
