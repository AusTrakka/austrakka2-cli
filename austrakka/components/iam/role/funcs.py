from austrakka.components.iam.shared_funcs import _get_default_tenant_global_id, _get_role_by_name
from austrakka.utils.api import api_get, api_post, api_patch
from austrakka.utils.enums.privilege_level import (
    AUSTRAKKA_ADMIN_LEVEL,
    FUNCTIONAL_ADMIN_LEVEL,
    USER_LEVEL)

from austrakka.utils.misc import logger_wraps
from austrakka.utils.output import print_dict


@logger_wraps()
def get_roles(out_format: str):
    """
    Get the list of roles defined for a tenant.
    """
    tenant_global_id = _get_default_tenant_global_id()
    response = api_get(
        path=f"v2/tenant/{tenant_global_id}/role",
    )

    data = response['data'] if ('data' in response) else response
    print_dict(
        data,
        out_format,
    )


@logger_wraps()
def add_role(role: str, description: str, privilege_level: str, allowed_record_types: list[str]):
    """
    Add a new role to a tenant.
    """
    # switch statement to map string name to integer value
    level = _privilege_name_to_int()
    tenant_global_id = _get_default_tenant_global_id()
    payload = {
        "name": role,
        "description": description,
        "privilegeLevel": level[privilege_level],
    }

    _assign_allowed_role_root_types(allowed_record_types, payload, tenant_global_id)

    api_post(
        path=f"v2/tenant/{tenant_global_id}/role",
        data=payload,
    )


@logger_wraps()
def update_role(
        role: str,
        new_name: str,
        description: str,
        privilege_level: str,
        allowed_record_types: list[str],
        clear_allowed_record_types: bool):
    """
    Update a role.
    """
    if (not new_name and
            not description and
            not privilege_level and
            not allowed_record_types and
            not clear_allowed_record_types):
        raise ValueError("At least one of new_name, description, privilege_level, "
                         "clear_allowed_record_types, or allowed_record_types must be provided")

    tenant_global_id = _get_default_tenant_global_id()
    role_obj = _get_role_by_name(role, tenant_global_id)

    payload = {}
    if new_name:
        payload["name"] = new_name

    if description:
        payload["description"] = description

    if privilege_level:
        level = _privilege_name_to_int()
        payload["privilegeLevel"] = level[privilege_level]

    if not clear_allowed_record_types and allowed_record_types:
        _assign_allowed_role_root_types(allowed_record_types, payload, tenant_global_id)

    if clear_allowed_record_types:
        payload["AllowedRootTypeGlobalIds"] = []

    api_patch(
        path=f"v2/tenant/{tenant_global_id}/role/{role_obj['globalId']}",
        data=payload,
    )


def _assign_allowed_role_root_types(allowed_record_types, payload, tenant_global_id):
    root_types = api_get(
        path=f"v2/tenant/{tenant_global_id}/roottype",
    )
    # Match allowed record types to root types by name.
    # Gather the global ID of the root type into a list.
    allowed_record_types_global_ids = []
    for record_type in allowed_record_types:
        record_type_obj = next((r for r in root_types['data'] if r['name'] == record_type), None)
        if record_type_obj is None:
            raise ValueError(f"Record type {record_type} not found in tenant {tenant_global_id}")
        allowed_record_types_global_ids.append(record_type_obj['globalId'])
    if len(allowed_record_types_global_ids) > 0:
        payload["AllowedRootTypeGlobalIds"] = allowed_record_types_global_ids


def _privilege_name_to_int():
    level = {
        AUSTRAKKA_ADMIN_LEVEL: 10000,
        FUNCTIONAL_ADMIN_LEVEL: 20000,
        USER_LEVEL: 30000,
    }
    return level
