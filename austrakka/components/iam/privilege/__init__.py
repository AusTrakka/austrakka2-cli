import click

from austrakka.components.iam.privilege.funcs import list_privileges, list_by_role_privileges, list_by_user_privileges, \
    grant_privilege, deny_privilege
from austrakka.utils.cmd_filter import hide_admin_cmds
from austrakka.utils.options import opt_record_type, opt_role, opt_user_object_id, opt_record_global_id
from austrakka.utils.output import table_format_option


@click.group()
@click.pass_context
def privilege(ctx):
    """Commands related to already assigned privileges."""
    ctx.context = ctx.parent.context


@privilege.command('list', hidden=hide_admin_cmds())
@opt_record_type()
@click.argument('record-global-id', type=str)
@table_format_option()
def privilege_list(record_type: str, record_global_id: str, out_format: str):
    """
    List the privileges assigned to a record.
    """
    list_privileges(record_type, record_global_id, out_format)


@privilege.command('list-by-role', hidden=hide_admin_cmds())
@opt_role()
@opt_record_type()
@click.argument('record-global-id', type=str)
@table_format_option()
def privilege_list_by_role(role: str, record_type: str, record_global_id: str, out_format: str):
    """
    List the privileges assigned to a record.
    """
    list_by_role_privileges(role, record_type, record_global_id, out_format)


@privilege.command('list-by-user', hidden=hide_admin_cmds())
@opt_user_object_id()
@opt_record_type()
@click.argument('record-id', type=str)
@table_format_option()
def privilege_list_by_user(user_id: str, record_type: str, record_id: str, out_format: str):
    """
    List the privileges assigned to a record.
    """
    list_by_user_privileges(user_id, record_type, record_id, out_format)


@privilege.command('grant', hidden=hide_admin_cmds())
@opt_user_object_id()
@opt_role()
@opt_record_global_id()
@opt_record_type()
def privilege_grant(
        user_id: str,
        role: str,
        record_global_id: str,
        record_type: str):
    """
    Grant a user access to a record limited by their role.
    """
    grant_privilege(user_id, role, record_global_id, record_type)


@privilege.command('deny', hidden=hide_admin_cmds())
@opt_record_global_id()
@opt_record_type()
@click.argument('privilege-global-id', type=str)
def privilege_deny(
        record_global_id: str,
        record_type: str,
        privilege_global_id: str):
    """
    Deny a user access to a record. Ie, remove the access if it was previously granted.
    """
    deny_privilege(record_global_id, record_type, privilege_global_id)
