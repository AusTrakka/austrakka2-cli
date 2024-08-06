from austrakka.components.iam.shared_funcs import _get_default_tenant, _get_role_by_name
from austrakka.utils.api import api_get, api_post, api_patch
from austrakka.utils.enums.privilege_level import *
from austrakka.utils.misc import logger_wraps
from austrakka.utils.output import print_dict


@logger_wraps()
def get_roles(out_format: str):
    """
    Get the list of roles defined for a tenant.
    """
    tenant_global_id = _get_default_tenant()
    response = api_get(
        path=f"v2/tenant/{tenant_global_id}/role",
    )

    data = response['data'] if ('data' in response) else response
    print_dict(
        data,
        out_format,
    )


@logger_wraps()
def add_role(role: str, description: str, privilege_level: str):
    """
    Add a new role to a tenant.
    """
    # switch statement to map string name to integer value
    level = _privilege_name_to_int()
    tenant_global_id = _get_default_tenant()
    payload = {
        "name": role,
        "description": description,
        "privilegeLevel": level[privilege_level],
    }

    api_post(
        path=f"v2/tenant/{tenant_global_id}/role",
        data=payload,
    )


@logger_wraps()
def update_role(role: str, new_name: str, description: str, privilege_level: str):
    """
    Update a role.
    """
    if not new_name and not description and not privilege_level:
        raise ValueError("At least one of new_name, description or privilege_level must be provided")

    tenant_global_id = _get_default_tenant()
    role_obj = _get_role_by_name(role, tenant_global_id)

    payload = {}
    if new_name:
        payload["name"] = new_name

    if description:
        payload["description"] = description

    if privilege_level:
        level = _privilege_name_to_int()
        payload["privilegeLevel"] = level[privilege_level]

    api_patch(
        path=f"v2/tenant/{tenant_global_id}/role/{role_obj['globalId']}",
        data=payload,
    )


def _privilege_name_to_int():
    level = {
        AUSTRAKKA_ADMIN_LEVEL: 10000,
        FUNCTIONAL_ADMIN_LEVEL: 20000,
        USER_LEVEL: 30000,
    }
    return level
