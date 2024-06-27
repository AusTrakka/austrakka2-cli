import click
from austrakka.utils.cmd_filter import hide_admin_cmds
from austrakka.utils.options import *
from austrakka.utils.output import table_format_option
from .funcs import get_roles, add_role, update_role


@click.group()
@click.pass_context
def role(ctx):
    """Commands related to role based access control"""
    ctx.context = ctx.parent.context


@role.command('get', hidden=hide_admin_cmds())
@opt_tenant_id()
@table_format_option()
def roles_get(tenant_id: str, out_format: str):
    """
    Get the list of roles defined for a tenant.
    """
    get_roles(tenant_id, out_format)


@role.command('add', hidden=hide_admin_cmds())
@opt_role()
@opt_description()
@opt_tenant_id()
def role_add(role: str, description: str, tenant_id: str):
    """
    Add a new role to the tenant.
    """
    add_role(role, description, tenant_id)


@role.command('update', hidden=hide_admin_cmds())
@opt_role()
@opt_tenant_id()
@opt_new_name(required=False)
@opt_description(required=False)
def role_update(role: str, tenant_id: str, new_name: str, description: str):
    """
    Update a role.
    """
    update_role(role, tenant_id, new_name, description)