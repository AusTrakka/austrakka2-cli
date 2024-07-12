from austrakka.utils.api import api_get, api_post, api_patch
from austrakka.utils.misc import logger_wraps
from austrakka.utils.output import print_dict


@logger_wraps()
def get_roles(tenant_id: str, out_format: str):
    """
    Get the list of roles defined for a tenant.
    """
    response = api_get(
        path=f"v2/tenant/{tenant_id}/role",
    )

    data = response['data'] if ('data' in response) else response
    print_dict(
        data,
        out_format,
    )


@logger_wraps()
def add_role(role: str, description: str, tenant_id: str):
    """
    Add a new role to a tenant.
    """
    payload = {
        "name": role,
        "description": description,
    }

    api_post(
        path=f"v2/tenant/{tenant_id}/role",
        data=payload,
    )


@logger_wraps()
def update_role(role: str, tenant_id: str, new_name: str, description: str):
    """
    Update a role.
    """
    existing_roles = api_get(
        path=f"v2/tenant/{tenant_id}/role",
    )

    role_obj = next((r for r in existing_roles['data'] if r['name'] == role), None)

    payload = {
        "name": new_name,
        "description": description,
    }

    api_patch(
        path=f"v2/tenant/{tenant_id}/role/{role_obj['roleId']}",
        data=payload,
    )
