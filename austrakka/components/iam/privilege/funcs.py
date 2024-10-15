from austrakka.utils.subcommands.shared_funcs import (
    get_role_by_name,
    get_privileges_by_user)

from austrakka.utils.api import api_get, api_delete, api_post
from austrakka.utils.helpers.tenant import get_default_tenant_global_id
from austrakka.utils.misc import logger_wraps
from austrakka.utils.output import print_dict


@logger_wraps()
def list_privileges(record_type: str, record_global_id: str, out_format: str):
    """
    List the privileges assigned to a record.
    """
    tenant_global_id = get_default_tenant_global_id()
    path = f"v2/{record_type}/{record_global_id}/privilege/?owningTenantGlobalId={tenant_global_id}"

    response = api_get(
        path=path,
    )

    _print_response_data(out_format, response)


@logger_wraps()
def list_by_role_privileges(role: str, record_type: str, record_global_id: str, out_format: str):
    """
    List by role the privileges assigned to a record.
    """
    tenant_global_id = get_default_tenant_global_id()
    roles = api_get(path=f"v2/tenant/{tenant_global_id}/role")
    role_obj = next((r for r in roles['data'] if r['name'] == role), None)

    if role_obj is None:
        raise ValueError(f"Role {role} not found in tenant {tenant_global_id}")

    role_global_id = role_obj['globalId']

    response = api_get(
        path=f"v2/{record_type}/{record_global_id}/privilege/role/{role_global_id}"
             f"?owningTenantGlobalId={tenant_global_id}",
    )

    _print_response_data(out_format, response)


@logger_wraps()
def list_by_user_privileges(user_id: str, record_type: str, record_global_id: str, out_format: str):
    """
    List by user the privileges assigned to a record.
    """
    tenant_global_id = get_default_tenant_global_id()
    response = get_privileges_by_user(user_id, record_type, record_global_id, tenant_global_id)
    _print_response_data(out_format, response)


@logger_wraps()
def assign_privilege(
        user_id: str,
        role: str,
        record_global_id: str,
        record_type: str):

    owning_tenant_global_id = get_default_tenant_global_id()
    role_obj = get_role_by_name(role, owning_tenant_global_id)

    payload = {
        "owningTenantGlobalId": owning_tenant_global_id,
        "roleGlobalId": role_obj['globalId'],
        "assigneeObjectId": user_id
    }

    uri_path = f"v2/{record_type}/{record_global_id}/privilege"
    return api_post(
        path=uri_path,
        data=payload,
    )


@logger_wraps()
def unassign_privilege(
        record_global_id: str,
        record_type: str,
        privilege_global_id: str):

    owning_tenant_global_id = get_default_tenant_global_id()
    uri_path = (f"v2/{record_type}/{record_global_id}/privilege/"
                f"{privilege_global_id}/?owningTenantGlobalId={owning_tenant_global_id}")

    api_delete(
        path=uri_path,
        custom_headers={}
    )


def _print_response_data(out_format, response):
    data = response['data'] if ('data' in response) else response
    print_dict(
        data,
        out_format,
    )
