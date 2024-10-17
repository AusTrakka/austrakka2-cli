from austrakka.utils.api import api_get, api_post, api_delete
from austrakka.utils.helpers.tenant import get_default_tenant_global_id
from austrakka.utils.misc import logger_wraps
from austrakka.utils.output import print_response

list_compact_fields = [
    'roleName', 
    'scopePath', 
    'scopeRootType', 
    'scopeShortDescription', 
    'roleGlobalId']

list_more_fields = [
    'roleName', 
    'scopePath', 
    'scopeRootType', 
    'scopeShortDescription', 
    'roleGlobalId', 
    'globalId', 
    'scopeDescription']


# pylint: disable=duplicate-code
@logger_wraps()
def get_role_definition(role: str, view_type: str, out_format: str):
    """
    Get the list of scope access defined for a role.
    """
    tenant_global_id = get_default_tenant_global_id()
    resp = api_get(path=f"v2/tenant/{tenant_global_id}/role")
    role_global_id = _get_role_global_id_by_name(resp, role, tenant_global_id)

    resp2 = api_get(
        path=f"v2/tenant/{tenant_global_id}/role/{role_global_id}/ScopeAccessDefinition",
    )

    print_response(
        resp2,
        view_type,
        list_compact_fields,
        list_more_fields,
        out_format,
    )


@logger_wraps()
def add_role_definition(role: str, global_ids: list[str]):
    """
    Add a new access definition to a role.
    """
    tenant_global_id = get_default_tenant_global_id()
    resp = api_get(path=f"v2/tenant/{tenant_global_id}/role",)
    role_global_id = _get_role_global_id_by_name(resp, role, tenant_global_id)

    api_post(
        path=f"v2/tenant/{tenant_global_id}/role/{role_global_id}/ScopeAccessDefinition",
        data=global_ids,
    )


@logger_wraps()
def remove_role_definition(scope_access_def_global_id: str):
    """
    Remove access from a role.
    """
    tenant_global_id = get_default_tenant_global_id()
    api_delete(
        path=f"v2/tenant/{tenant_global_id}/role/ScopeAccessDefinition/"
             f"{scope_access_def_global_id}",
        custom_headers={}
    )


def _get_role_global_id_by_name(resp, role, tenant_global_id):
    if 'data' in resp:
        roles = resp['data']
        role_obj = next((r for r in roles if r['name'] == role), None)
        if role_obj is None:
            raise ValueError(f"Role {role} not found in tenant {tenant_global_id}")
        return role_obj['globalId']

    raise ValueError("Could not get role information from server. Received nil data.")
