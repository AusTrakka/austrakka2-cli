from austrakka.utils.api import api_get


def _get_default_tenant_global_id():
    default_tenant = api_get(path="v2/tenant/default")
    tenant_global_id = default_tenant['data']['globalId']
    if not tenant_global_id:
        raise ValueError("Default tenant not found")

    return tenant_global_id


def _get_role_by_name(role, tenant_global_id):
    existing_roles = api_get(
        path=f"v2/tenant/{tenant_global_id}/role",
    )
    role_obj = next((r for r in existing_roles['data'] if r['name'] == role), None)
    return role_obj
