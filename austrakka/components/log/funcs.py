from austrakka.utils.api import api_get
from austrakka.utils.misc import logger_wraps
from austrakka.utils.output import print_dataframe, read_pd, get_viewtype_columns
from austrakka.utils.privilege import get_priv_path
from austrakka.utils.datetimes import dt_parse

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
        event_type: str,
        submitter: str,
        resource_identifier: str,
        resource_type: str,
        out_format: str,
        view_type: str,
        ):
    params = {}
    if start is not None:
        params["startDateTime"] = dt_parse(start)
    if end is not None:
        params["endDateTime"] = dt_parse(end)
    if event_type is not None:
        params["eventType"] = event_type
    if submitter is not None:
        params["submitterDisplayName"] = submitter
    if resource_identifier is not None:
        params["resourceIdentifier"] = resource_identifier
    if resource_type is not None:
        params["resourceType"] = resource_type

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
