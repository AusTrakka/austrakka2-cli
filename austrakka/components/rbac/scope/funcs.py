from austrakka.utils.api import api_get
from austrakka.utils.misc import logger_wraps
from austrakka.utils.output import print_dict


@logger_wraps()
def get_scope(tenant_id: str, out_format: str):
    """
    Get the list of scopes defined for a tenant.
    """
    response = api_get(
        path=f"v2/tenant/{tenant_id}/scope",
    )

    data = response['data'] if ('data' in response) else response
    print_dict(
        data,
        out_format,
    )