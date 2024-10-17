from austrakka.utils.api import api_get

def get_role_by_name(role, tenant_global_id):
    existing_roles = api_get(
        path=f"v2/tenant/{tenant_global_id}/role",
    )
    role_obj = next((r for r in existing_roles['data'] if r['name'] == role), None)
    return role_obj


def get_privileges_by_user(
        user_id: str,
        record_type: str,
        record_global_id: str,
        tenant_global_id: str):
    """
    List by user the privileges assigned to a record.
    """
    return api_get(
        path=f"v2/{record_type}/{record_global_id}/privilege/user/{user_id}"
             f"?owningTenantGlobalId={tenant_global_id}",
    )
