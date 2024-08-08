import click
from austrakka.utils.cmd_filter import hide_admin_cmds
from austrakka.utils.options import *
from austrakka.utils.output import table_format_option
from .access import access
from .funcs import get_roles, add_role, update_role


@click.group()
@click.pass_context
def role(ctx):
    """Commands related to role based access control"""
    ctx.context = ctx.parent.context


role.add_command(access)


@role.command('get', hidden=hide_admin_cmds())
@table_format_option()
def roles_get(out_format: str):
    """
    Get the list of roles defined for a tenant.
    """
    get_roles(out_format)


@role.command('add', hidden=hide_admin_cmds())
@opt_role()
@opt_description()
@opt_privilege_level()
def role_add(role: str, description: str, privilege_level: str):
    """
    Add a new role to the tenant.
    """
    add_role(role, description, privilege_level)


@role.command('update', hidden=hide_admin_cmds())
@opt_role()
@opt_new_name(required=False)
@opt_description(required=False)
@opt_privilege_level(required=False)
def role_update(role: str, new_name: str, description: str, privilege_level: str):
    """
    Update a role.
    """
    update_role(role, new_name, description, privilege_level)
