from austrakka.utils.api import api_post, api_get
from austrakka.utils.misc import logger_wraps

supported_record_types = ["tenant"]


@logger_wraps()
def grant_role(
        user_id: str,
        role: str,
        tenant_id: str,
        record_type: str,
        record_id: str):

    if record_type not in supported_record_types:
        raise ValueError(f"Unsupported record type: {record_type}. "
                         f"Supported record types: {supported_record_types}")

    tenant = _get_tenant_name(tenant_id)
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


def _get_tenant_name(tenant_id: str) -> str:
    return api_get(
        path=f"v2/tenant/{tenant_id}",
    )
