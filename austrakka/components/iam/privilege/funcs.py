from austrakka.utils.api import api_get, api_delete, api_post
from austrakka.utils.misc import logger_wraps
from austrakka.utils.output import print_dict

supported_record_types = ["tenant"]


@logger_wraps()
def list_privileges(tenant_id: str, record_type: str, record_id: str, out_format: str):
    """
    List the privileges assigned to a record.
    """
    if record_type not in supported_record_types:
        raise ValueError(f"Unsupported record type: {record_type}. "
                         f"Supported record types: {supported_record_types}")

    response = api_get(
        path=f"v2/{record_type}/{record_id}/privilege/?owningTenantId={tenant_id}",
    )

    data = response['data'] if ('data' in response) else response

    print_dict(
        data,
        out_format,
    )


@logger_wraps()
def list_by_role_privileges(tenant_id: str, role: str, record_type: str, record_id: str, out_format: str):
    """
    List by role the privileges assigned to a record.
    """
    if record_type not in supported_record_types:
        raise ValueError(f"Unsupported record type: {record_type}. "
                         f"Supported record types: {supported_record_types}")

    roles = api_get(
        path=f"v2/tenant/{tenant_id}/role",
    )

    role_obj = next((r for r in roles['data'] if r['name'] == role), None)

    if role_obj is None:
        raise ValueError(f"Role {role} not found in tenant {tenant_id}")

    role_id = role_obj['roleId']

    response = api_get(
        path=f"v2/{record_type}/{record_id}/privilege/role/{role_id}?owningTenantId={tenant_id}",
    )

    data = response['data'] if ('data' in response) else response

    print_dict(
        data,
        out_format,
    )


@logger_wraps()
def list_by_user_privileges(user_id: str, tenant_id: str, record_type: str, record_id: str, out_format: str):
    """
    List by user the privileges assigned to a record.
    """
    if record_type not in supported_record_types:
        raise ValueError(f"Unsupported record type: {record_type}. "
                         f"Supported record types: {supported_record_types}")

    response = api_get(
        path=f"v2/{record_type}/{record_id}/privilege/user/{user_id}?owningTenantId={tenant_id}",
    )

    data = response['data'] if ('data' in response) else response

    print_dict(
        data,
        out_format,
    )


@logger_wraps()
def grant_privilege(
        user_id: str,
        role: str,
        record_id: str,
        record_type: str,
        owning_tenant_id: str):

    if record_type not in supported_record_types:
        raise ValueError(f"Unsupported record type: {record_type}. "
                         f"Supported record types: {supported_record_types}")

    tenant = _get_root_record('tenant', owning_tenant_id)
    tenant_name = tenant["data"]['name']

    payload = {
        "owningTenantName": tenant_name,
        "roleName": role,
        "assigneeObjectId": user_id
    }

    uri_path = f"v2/{record_type}/{record_id}/privilege"
    return api_post(
        path=uri_path,
        data=payload,
    )


@logger_wraps()
def deny_privilege(
        record_id: str,
        record_type: str,
        owning_tenant_id: str,
        privilege_id: str):

    if record_type not in supported_record_types:
        raise ValueError(f"Unsupported record type: {record_type}. "
                         f"Supported record types: {supported_record_types}")

    uri_path = f"v2/{record_type}/{record_id}/privilege/{privilege_id}/?owningTenantId={owning_tenant_id}"

    api_delete(
        path=uri_path,
        custom_headers={}
    )


def _get_root_record(root_record_type: str, root_record_id: str) -> str:
    return api_get(
        path=f"v2/{root_record_type}/{root_record_id}",
    )


def _get_privilege_by_user_id(user_id: str, record_type: str, record_id: str, tenant_id: str):
    uri_path = f"v2/{record_type}/{record_id}/privilege/User/{user_id}/?owningTenantId={tenant_id}"
    return api_get(
        path=uri_path
    )
