import json
from austrakka.utils.add_filters import add_equals_filter
from austrakka.utils.api import api_get
from austrakka.utils.misc import logger_wraps
from austrakka.utils.output import print_dataframe, read_pd, get_viewtype_columns
from austrakka.utils.privilege import get_priv_path

COMPACT_FIELDS = ['eventTime','resourceType','resourceName','eventType',
                  'eventStatus','submitterDisplayName']
MORE_FIELDS = ['clientSessionId','callId','globalId']
FIELD_ORDERING = ['globalId'] + COMPACT_FIELDS + ['callId','clientSessionId']

# pylint: disable=duplicate-code
@logger_wraps()
def list_logs(
        record_type: str,
        record_global_id: str,
        start: str,
        end: str,
        submitter: str,
        resource: str,
        resource_type: str,
        out_format: str,
        view_type: str,
        ):
    params = {}
    filters = {}
    # if start is not None:
        # params["startDateTime"] = dt_parse(start)
    # if end is not None:
        # params["endDateTime"] = dt_parse(end)
    add_equals_filter(filters, "submitterDisplayName", submitter)
    add_equals_filter(filters, "resourceUniqueString", resource)
    add_equals_filter(filters, "resourceType", resource_type)

    params["filters"] = json.dumps(filters)

    response = api_get(
        path=f"{get_priv_path(record_type, record_global_id)}/ActivityLog",
        params=params
    )
    
    result = read_pd(response['data'], out_format)
    result.rename(columns={'resourceUniqueString': 'resourceName'}, inplace=True)

    # Unordered fields will be at end.
    result = result[FIELD_ORDERING + [col for col in result.columns if col not in FIELD_ORDERING]]
    
    display_cols = get_viewtype_columns(view_type, COMPACT_FIELDS, MORE_FIELDS)
    print_dataframe(
        result,
        out_format,
        restricted_cols=display_cols
    )
