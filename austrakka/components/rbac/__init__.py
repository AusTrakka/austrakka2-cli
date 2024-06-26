import click
from austrakka.utils.cmd_filter import hide_admin_cmds
from austrakka.utils.options import *
from .funcs import grant_role
from .scope import scope
from .role import role


@click.group()
@click.pass_context
def rbac(ctx):
    """Commands related to role based access control"""
    ctx.context = ctx.parent.context


rbac.add_command(scope)
rbac.add_command(role)


@rbac.command('grant', hidden=hide_admin_cmds())
@opt_user_object_id()
@opt_role()
@opt_tenant_id()
@opt_record_type()
@click.argument('record-id', type=str)
def rbac_grant(
        user_id: str,
        role: str,
        tenant_id: str,
        record_type: str,
        record_id: str):
    """
    Grant a user access to a record limited by their role.
    """
    grant_role(user_id, role, tenant_id, record_type, record_id)