import click
from austrakka.utils.cmd_filter import hide_admin_cmds
from austrakka.utils.options import *
from austrakka.utils.output import table_format_option
from .definition import definition
from .funcs import list_roles, add_role, update_role, delete_role


@click.group()
@click.pass_context
def role(ctx):
    """Commands related to role based access control"""
    ctx.context = ctx.parent.context


role.add_command(definition)


@role.command('list', hidden=hide_admin_cmds())
@opt_view_type()
@table_format_option()
def roles_list(view_type: str, out_format: str):
    """
    Get the list of roles
    """
    list_roles(view_type, out_format)


# pylint: disable=redefined-outer-name
@role.command('add', hidden=hide_admin_cmds())
@opt_role()
@opt_description()
@opt_privilege_level()
@opt_record_type(
    required=False, 
    multiple=True, 
    help="Name of each allowed record types where a role can be used to control access."
)
def role_add(
        role: str,
        description: str,
        privilege_level: str,
        record_type: list[str]):
    """
    Add a new role
    """
    add_role(role, description, privilege_level, record_type)


# pylint: disable=expression-not-assigned,duplicate-code
# pylint: disable=redefined-outer-name
@role.command('update', hidden=hide_admin_cmds())
@opt_role()
@opt_new_name(required=False)
@opt_description(required=False)
@opt_privilege_level(required=False)
@create_option('-art',
               '--allowed-record-types',
               help='Name of each allowed record types where a role can be used to control access.',
               cls=MutuallyExclusiveOption,
               multiple=True,
               mutually_exclusive=["clear_allowed_record_types"],
               required=False)
@create_option('-clr',
               '--clear-allowed-record-types',
               cls=MutuallyExclusiveOption,
               help="Clear the list of allowed record types current set on the role.",
               type=click.BOOL,
               mutually_exclusive=["allowed_record_types"],
               required=False,
               is_flag=True)
def role_update(
        role: str,
        new_name: str,
        description: str,
        privilege_level: str,
        allowed_record_types: list[str],
        clear_allowed_record_types: bool):
    """
    Update a role
    """
    update_role(
        role,
        new_name,
        description,
        privilege_level,
        allowed_record_types,
        clear_allowed_record_types)


# pylint: disable=redefined-outer-name
@role.command('remove', hidden=hide_admin_cmds())
@opt_role()
@create_option('--no-confirm',
               help='Skip confirmation prompt',
               is_flag=True,
               default=False)
def role_remove(role: str, no_confirm: bool):
    """
    Remove a role
    """
    if not no_confirm:
        if not click.confirm(f'Are you sure you want to remove role "{role}"?'):
            click.echo('Operation cancelled.')
            return
    
    delete_role(role)
