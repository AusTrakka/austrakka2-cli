
import click

from austrakka.utils.privilege import TENANT_RESOURCE
from austrakka.utils.cmd_filter import hide_admin_cmds
from austrakka.utils.options import (
    opt_role,
    opt_user_identifier,
    opt_identifier)
from austrakka.utils.output import table_format_option
from .funcs import (
    list_privileges,
    list_by_role_privileges,
    list_by_user_privileges,
    assign_privilege,
    unassign_privilege,
)



def privilege_subcommands(root_type: str):
    """
    Generate privilege subcommands for a given root type.
    """
    root_type_name = 'system' if root_type == TENANT_RESOURCE else root_type.lower()

    @click.group(help=f"Commands related to {root_type_name} privileges")
    @click.pass_context
    def privilege(ctx):
        ctx.context = ctx.parent.context

    @privilege.command('list', 
                       help="List all system-level privilege assignments"
                            if root_type == TENANT_RESOURCE else
                            f"List all privilege assignments for the {root_type_name}",
                       hidden=hide_admin_cmds())
    @( # This adds the identifier parameter only if the root_type is not tenant
        opt_identifier(
            required=True,
            help=f"Identifier of the {root_type_name} for which to list privileges")
        if root_type != TENANT_RESOURCE else lambda f: f
    )
    @table_format_option()
    def privilege_list(out_format: str, identifier:str=None):
        list_privileges(root_type, identifier, out_format)


    @privilege.command('list-by-role',
                       help=f"List all users who hold a specific "
                            f"role in the {root_type_name}.",
                       hidden=hide_admin_cmds())
    @opt_role()
    @( # This adds the identifier parameter only if the root_type is not tenant
         opt_identifier(
             required=True,
             help=f"Identifier of the {root_type_name} for which to list privileges")
         if root_type != TENANT_RESOURCE else lambda f: f
    )
    @table_format_option()
    def privilege_list_by_role(role: str, out_format: str, identifier:str=None):
        list_by_role_privileges(role, root_type, identifier, out_format)


    @privilege.command('list-by-user',
                        help=f"List all roles held by a specific "
                             f"user for the {root_type_name}.",
                        hidden=hide_admin_cmds())
    @opt_user_identifier()
    @( # This adds the identifier parameter only if the root_type is not tenant
        opt_identifier(
            required=True,
            help=f"Identifier of the {root_type_name} for which to list privileges")
        if root_type != TENANT_RESOURCE else lambda f: f
    )
    @table_format_option()
    def privilege_list_by_user(user_id: str, out_format: str, identifier:str=None):
        list_by_user_privileges(user_id, root_type, identifier, out_format)


    @privilege.command('assign',
                        help=f"Assign {root_type_name}-level privileges to a user",
                        hidden=hide_admin_cmds())
    @opt_user_identifier()
    @opt_role()
    @( # This adds the identifier parameter only if the root_type is not tenant
        opt_identifier(
            required=True,
            help=f"Identifier of the {root_type_name} to grant access to")
        if root_type != TENANT_RESOURCE else lambda f: f
    )
    def privilege_assign(
            user_id: str,
            role: str,
            identifier: str = None):
        assign_privilege(user_id, role, identifier, root_type)


    @privilege.command('unassign',
                        help=f"Remove {root_type_name}-level privileges from a user",
                        hidden=hide_admin_cmds())
    @opt_user_identifier()
    @opt_role()
    @( # This adds the identifier parameter only if the root_type is not tenant
        opt_identifier(
            required=True,
            help=f"Identifier of the {root_type_name} to remove access to")
        if root_type != TENANT_RESOURCE else lambda f: f
    )
    def privilege_unassign(
            user_id: str,
            role: str,
            identifier: str = None):
        unassign_privilege(user_id, role, identifier, root_type)

    return privilege
