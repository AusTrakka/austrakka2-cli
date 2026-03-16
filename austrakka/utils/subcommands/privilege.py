
import click

from austrakka.components.iam.privilege.funcs import (
    list_privileges,
    list_by_role_privileges,
    list_by_user_privileges,
    assign_privilege,
    unassign_privilege,
)
from austrakka.utils.cmd_filter import hide_admin_cmds
from austrakka.utils.options import (
    opt_role,
    opt_user_global_id, opt_identifier)
from austrakka.utils.output import table_format_option


def privilege_subcommands(roottype: str):
    """
    Generate privilege subcommands for a given root type.
    """
    @click.group(help=f"Commands related to {roottype.lower()} privileges")
    @click.pass_context
    def privilege(ctx):
        ctx.context = ctx.parent.context

    @privilege.command('list', 
                       help=f"List all privileges held within a given {roottype.lower()}.",
                       hidden=hide_admin_cmds())
    @opt_identifier()
    @table_format_option()
    def privilege_list(global_id: str, out_format: str):
        list_privileges(roottype, global_id, out_format)


    @privilege.command('list-by-role',
                       help=f"List all users who hold a specific "
                            f"role in a given {roottype.lower()}.",
                       hidden=hide_admin_cmds())
    @opt_role()
    @opt_identifier()
    @table_format_option()
    def privilege_list_by_role(role: str, global_id: str, out_format: str):
        list_by_role_privileges(role, roottype, global_id, out_format)


    @privilege.command('list-by-user',
                        help=f"List all roles held by a specific "
                             f"user for a given {roottype.lower()}.",
                        hidden=hide_admin_cmds())
    @opt_identifier(option_name="--user-id", var_name="user_id", help="User identifier")
    @opt_identifier()
    @table_format_option()
    def privilege_list_by_user(user_id: str, global_id: str, out_format: str):
        list_by_user_privileges(user_id, roottype, global_id, out_format)


    @privilege.command('assign',
                        help=f"Assign privileges to access a {roottype.lower()} to a user.",
                        hidden=hide_admin_cmds())
    @opt_identifier(option_name="--user-id", var_name="user_id", help="User identifier")
    @opt_role()
    @opt_identifier()
    def privilege_assign(
            user_id: str,
            role: str,
            global_id: str):
        assign_privilege(user_id, role, global_id, roottype)


    @privilege.command('unassign',
                        help=f"Remove privileges to access a {roottype.lower()} from a user.",
                        hidden=hide_admin_cmds())
    @opt_identifier(option_name="--user-id", var_name="user_id", help="User identifier")
    @opt_role()
    @opt_identifier()
    def privilege_unassign(
            user_id: str,
            role: str,
            global_id: str):
        unassign_privilege(user_id, role, global_id, roottype)

    return privilege
