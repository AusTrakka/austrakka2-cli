from austrakka.utils.api import api_get, api_post, api_patch


def get_default_tenant_global_id():
    return _get_default_tenant_global_id()


def request_interaction_window(scope_alias: str, specificity_obj: dict):

    global_id = _get_default_tenant_global_id()
    resp = api_post(
        path=f"v2/tenant/{global_id}/interactionWindow",
        data={
            "scopeAlias": scope_alias,
            "specificityProps": specificity_obj
        })
    return resp['data']


def deactivate_interaction_window(window_id: str):
    global_id = _get_default_tenant_global_id()
    api_patch(
        path=f"v2/tenant/{global_id}/interactionWindow/{window_id}/disable",
        data={}
    )
    
    
def _get_default_tenant_global_id():
    default_tenant = api_get(path="v2/tenant/default")
    tenant_global_id = default_tenant['data']['globalId']
    if not tenant_global_id:
        raise ValueError("Default tenant not found")

    return tenant_global_id
