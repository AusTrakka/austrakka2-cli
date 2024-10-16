
import click

from austrakka.utils.helpers.tenant import get_default_tenant_global_id
from austrakka.utils.options import (
    opt_role,
    opt_user_object_id,
    opt_record_global_id)

from austrakka.utils.cmd_filter import hide_admin_cmds
from austrakka.utils.output import table_format_option
from austrakka.utils.privilege import convert_record_type_to_route_string

from austrakka.components.iam.privilege.funcs import (
    list_privileges,
    list_by_role_privileges,
    list_by_user_privileges,
    assign_privilege,
    unassign_privilege,
    get_privileges_by_user)


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
    @opt_record_global_id()
    @table_format_option()
    def privilege_list(record_global_id: str, out_format: str):
        record_type_route = convert_record_type_to_route_string(roottype)
        list_privileges(record_type_route, record_global_id, out_format)


    @privilege.command('list-by-role',
                       help=f"List all users who hold a specific "
                            f"role in a given {roottype.lower()}.",
                       hidden=hide_admin_cmds())
    @opt_role()
    @click.argument('record-global-id', type=str)
    @table_format_option()
    def privilege_list_by_role(role: str, record_global_id: str, out_format: str):
        record_type_route = convert_record_type_to_route_string(roottype)
        list_by_role_privileges(role, record_type_route, record_global_id, out_format)


    @privilege.command('list-by-user',
                        help=f"List all roles held by a specific "
                             f"user for a given {roottype.lower()}.",
                        hidden=hide_admin_cmds())
    @opt_user_object_id()
    @click.argument('record-global-id', type=str)
    @table_format_option()
    def privilege_list_by_user(user_id: str, record_global_id: str, out_format: str):
        record_type_route = convert_record_type_to_route_string(roottype)
        list_by_user_privileges(user_id, record_type_route, record_global_id, out_format)


    @privilege.command('assign',
                        help=f"Assign privileges to access a {roottype.lower()} to a user.",
                        hidden=hide_admin_cmds())
    @opt_user_object_id()
    @opt_role()
    @opt_record_global_id()
    def privilege_assign(
            user_id: str,
            role: str,
            record_global_id: str):
        record_type_route = convert_record_type_to_route_string(roottype)
        assign_privilege(user_id, role, record_global_id, record_type_route)


    @privilege.command('unassign',
                        help=f"Remove privileges to access a {roottype.lower()} from a user.",
                        hidden=hide_admin_cmds())
    @opt_record_global_id()
    @opt_role()
    @opt_user_object_id()
    def privilege_unassign(
            record_global_id: str,
            role: str,
            user_id: str):
    
        record_type_route = convert_record_type_to_route_string(roottype)
        tenant_global_id = get_default_tenant_global_id()
        
        user_privileges = get_privileges_by_user(
            user_id, 
            record_type_route, 
            record_global_id,
            tenant_global_id)
        
        # Get the first privilege that matches the role
        privilege_rec = next((p for p in user_privileges['data'] 
                              if p['role']['name'] == role), None)
    
        unassign_privilege(
            record_global_id, 
            record_type_route,
            privilege_rec['privilegeGlobalId'],
        )
    
    return privilege
