from austrakka.utils.api import api_get


def get_default_tenant_global_id():
    default_tenant = api_get(path="v2/tenant/default")
    tenant_global_id = default_tenant['data']['globalId']
    if not tenant_global_id:
        raise ValueError("Default tenant not found")

    return tenant_global_id
