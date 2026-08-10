import click
from trakka.utils.cmd_filter import hide_admin_cmds
from trakka.utils.options import *
from trakka.utils.output import table_format_option
from .scope import scope
from .funcs import list_roles, add_role, update_role, delete_role


@click.group()
@click.pass_context
def role(ctx):
    """Commands related to role based access control"""
    ctx.context = ctx.parent.context


role.add_command(scope)


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
@opt_resource_type(help="Type of the resource to which the role grants access.")
@opt_identifier('--scope', 'scopes', multiple=True, help="Scope ID")
def role_add(
        role: str,
        description: str,
        privilege_level: str,
        resource_type: str,
        scopes: list[str],
):
    """
    Add a new role
    """
    add_role(role, description, privilege_level, resource_type, scopes)


# pylint: disable=expression-not-assigned,duplicate-code
# pylint: disable=redefined-outer-name
@role.command('update', hidden=hide_admin_cmds())
@opt_role()
@opt_new_name(required=False)
@opt_description(required=False)
@opt_privilege_level(required=False)
@opt_resource_type(required=False, help="Type of the resource to which the role grants access.")
def role_update(
        role: str,
        new_name: str,
        description: str,
        privilege_level: str,
        resource_type: str):
    """
    Update a role
    """
    update_role(
        role,
        new_name,
        description,
        privilege_level,
        resource_type)



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
