from trakka.components.iam.role.scope.funcs import (
    add_role_scope,
    remove_role_scope)

from trakka.utils.cmd_filter import hide_admin_cmds
from trakka.utils.options import *


@click.group()
@click.pass_context
def scope(ctx):
    """Commands related to roles scopes."""
    ctx.context = ctx.parent.context


@scope.command('add', hidden=hide_admin_cmds())
@opt_role()
@opt_identifier('--scope', 'scopes', multiple=True, help="Scope ID")
def role_scope_add(role: str, scopes: list[str]):
    """
    Add scope to a role.
    """
    add_role_scope(role, scopes)


@scope.command('remove', hidden=hide_admin_cmds())
@opt_role()
@opt_identifier('--scope', 'scopes', multiple=True, help="Scope ID")
def role_scope_remove(role: str, scopes: list[str]):
    """
    Remove scope from a role.
    """
    remove_role_scope(role, scopes)
