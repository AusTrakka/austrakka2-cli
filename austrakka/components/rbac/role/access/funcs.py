from austrakka.utils.api import api_get, api_post, api_patch, api_delete
from austrakka.utils.misc import logger_wraps
from austrakka.utils.output import print_dict


@logger_wraps()
def get_access(tenant_id: str, role: str, out_format: str):
    """
    Get the list of scope access defined for a role.
    """
    resp = api_get(
        path=f"v2/tenant/{tenant_id}/role",
    )

    role_id = _get_role_id_by_name(resp, role, tenant_id)

    resp2 = api_get(
        path=f"v2/tenant/{tenant_id}/role/{role_id}/ScopeAccessDefinition",
    )

    data = resp2['data'] if ('data' in resp2) else resp2
    print_dict(
        data,
        out_format,
    )


@logger_wraps()
def add_access(tenant_id: str, role: str, ids: list[int]):
    """
    Add a new access definition to a role.
    """
    resp = api_get(
        path=f"v2/tenant/{tenant_id}/role",
    )

    role_id = _get_role_id_by_name(resp, role, tenant_id)

    api_post(
        path=f"v2/tenant/{tenant_id}/role/{role_id}/ScopeAccessDefinition",
        data=ids,
    )


def remove_access(tenant_id: str, scope_access_def_id: int):
    """
    Remove access from a role.
    """
    api_delete(
        path=f"v2/tenant/{tenant_id}/role/ScopeAccessDefinition/{scope_access_def_id}",
        custom_headers={}
    )


def _get_role_id_by_name(resp, role, tenant_id):
    if 'data' in resp:
        roles = resp['data']
        role_obj = next((r for r in roles if r['name'] == role), None)
        if role_obj is None:
            raise ValueError(f"Role {role} not found in tenant {tenant_id}")
        return role_obj['roleId']
    else:
        raise ValueError(f"Could not get role information from server. Received nil data.")
