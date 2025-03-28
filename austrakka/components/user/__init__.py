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
from austrakka.utils.options import opt_server_username
from austrakka import __prog_name__ as PROG_NAME
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


@user.command('list', help=f"List users in {PROG_NAME}")
@opt_show_disabled()
@table_format_option()
def user_list(show_disabled: bool, out_format: str):
    list_users(show_disabled, out_format)


@user.command('add', hidden=hide_admin_cmds(), help=f'Add users in {PROG_NAME}')
@opt_user_object_id()
@opt_organisation()
@opt_owner_group_roles(required=False)
@opt_is_austrakka_process(default=False)
@opt_server_username()
def user_add(
        user_id: str,
        org: str,
        owner_group_roles: List[str],
        is_process: bool,
        server_username: str,
):
    add_user(user_id, org, owner_group_roles, is_process, server_username)


@user.command('update', hidden=hide_admin_cmds(), help=f'Add users in {PROG_NAME}')
@opt_user_object_id()
@opt_name(help="Display Name", required=False)
@opt_email_address(required=False)
@opt_organisation(required=False)
@opt_is_active(required=False)
@opt_server_username(required=False)
def user_update(
    user_id: str,
    org: str,
    is_active: bool,
    email: str,
    name: str,
    server_username: str,
):
    update_user(user_id, name, email, org, server_username, is_active)


@user.command('enable', help=f"Re-enable a user in {PROG_NAME}")
@opt_user_object_id()
def user_enable(user_id: str):
    enable_user(user_id)


@user.command('disable', help=f"Disable a user in {PROG_NAME}")
@opt_user_object_id()
def user_disable(user_id: str):
    disable_user(user_id)
