from austrakka.utils.api import api_post, api_delete
from austrakka.utils.helpers.output import call_get_and_print
from austrakka.utils.misc import logger_wraps
from austrakka.utils.output import get_viewtype_columns
from austrakka.utils.paths import ROLES_V2_PATH
from austrakka.utils.subcommands.shared_funcs import get_role_global_id_by_name

list_compact_fields = [
    'roleName', 
    'scope', 
    'scopeRootType', 
    'roleGlobalId']

list_more_fields = [
    'roleName', 
    'scope', 
    'scopeRootType', 
    'roleGlobalId', 
    'globalId']


# pylint: disable=duplicate-code
@logger_wraps()
def list_role_definitions(role: str, view_type: str, out_format: str):
    """
    List scope access definitions defined for a role.
    """
    columns = get_viewtype_columns(view_type, list_compact_fields, list_more_fields)
    call_get_and_print(
        f"{ROLES_V2_PATH}/{get_role_global_id_by_name(role)}/ScopeAccessDefinition",
        out_format,
        restricted_cols=columns,
    )


@logger_wraps()
def add_role_definition(role: str, global_ids: list[str]):
    """
    Add a new access definition to a role.
    """
    api_post(
        path=f"{ROLES_V2_PATH}/{get_role_global_id_by_name(role)}/ScopeAccessDefinition",
        data=global_ids,
    )


@logger_wraps()
def remove_role_definition(scope_access_def_global_id: str):
    """
    Remove access from a role.
    """
    api_delete(
        path=f"{ROLES_V2_PATH}/ScopeAccessDefinition/"
             f"{scope_access_def_global_id}",
    )
