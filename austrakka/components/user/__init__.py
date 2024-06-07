from typing import List

import click

from austrakka.utils.output import table_format_option
from austrakka.utils.cmd_filter import hide_admin_cmds
from austrakka.utils.options import \
    opt_owner_group_roles, \
    opt_name, \
    opt_email_address, \
    opt_is_active
from austrakka.utils.options import opt_is_austrakka_process
from austrakka.utils.options import opt_user_object_id
from austrakka.utils.options import opt_organisation
from austrakka.utils.options import opt_show_disabled
from .funcs import list_users
from .funcs import add_user
from .funcs import update_user
from .funcs import enable_user
from .funcs import disable_user


@click.group()
@click.pass_context
def user(ctx):
    '''Commands related to users'''
    ctx.context = ctx.parent.context


@user.command('list')
@opt_show_disabled()
@table_format_option()
def user_list(show_disabled: bool, out_format: str):
    '''List users in AusTrakka'''
    list_users(show_disabled, out_format)


@user.command('add', hidden=hide_admin_cmds())
@opt_user_object_id()
@opt_organisation()
@opt_owner_group_roles(required=False)
@opt_is_austrakka_process(default=False)
def user_add(
        user_id: str,
        org: str,
        owner_group_roles: List[str],
        is_austrakka_process: bool,
):
    """Add users in AusTrakka"""
    add_user(user_id, org, owner_group_roles, is_austrakka_process)


@user.command('update', hidden=hide_admin_cmds())
@opt_user_object_id()
@opt_name(help="Display Name", required=False)
@opt_email_address(required=False)
@opt_organisation(required=False)
@opt_is_active(required=False)
def user_update(
    user_id: str,
    org: str,
    is_active: bool,
    email: str,
    name: str,
):
    """Add users in AusTrakka"""
    update_user(user_id, name, email, org, is_active)


@user.command('enable')
@opt_user_object_id()
def user_enable(user_id: str):
    """Re-enable a user in AusTrakka"""
    enable_user(user_id)


@user.command('disable')
@opt_user_object_id()
def user_disable(user_id: str):
    """Disable a user in AusTrakka"""
    disable_user(user_id)
