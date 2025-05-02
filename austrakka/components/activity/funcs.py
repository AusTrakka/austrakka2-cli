import pandas as pd

from austrakka.utils.api import api_get
from austrakka.utils.helpers.tenant import get_default_tenant_global_id
from austrakka.utils.misc import logger_wraps
from austrakka.utils.output import print_dataframe


@logger_wraps()
def get_activity(out_format: str):
    """
    Get the activity log for the platform.
    """
    tenant_global_id = get_default_tenant_global_id()
    response = api_get(
        path=f"v2/tenant/{tenant_global_id}/activitylog?owningTenantGlobalId={tenant_global_id}",
    )

    data = response['data'] if ('data' in response) else response
    result = pd.DataFrame.from_dict(data)

    print_dataframe(
        result,
        out_format,
    )
