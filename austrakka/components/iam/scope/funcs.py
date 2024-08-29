from austrakka.components.iam.shared_funcs import _get_default_tenant_global_id
from austrakka.utils.api import api_get
from austrakka.utils.misc import logger_wraps
from austrakka.utils.output import print_dict


@logger_wraps()
def get_scopes(out_format: str):
    """
    Get the list of scopes defined for a tenant.
    """
    tenant_global_id = _get_default_tenant_global_id()
    response = api_get(path=f"v2/tenant/{tenant_global_id}/scope")

    data = response['data'] if ('data' in response) else response
    print_dict(
        data,
        out_format,
    )
