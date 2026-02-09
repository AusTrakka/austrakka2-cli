
from austrakka.utils.api import api_get
from austrakka.utils.misc import logger_wraps
from austrakka.utils.output import print_dataframe, read_pd, get_viewtype_columns
from austrakka.utils.privilege import get_priv_path


@logger_wraps()
def list_logs(
        record_type: str,
        record_global_id: str,
        out_format: str,
        view_type: str):
    
    compact_fields = ['eventTime','resourceType','resourceName','eventType',
                      'eventStatus','submitterDisplayName']
    more_fields = ['clientSessionId','callId','globalId']

    field_ordering = ['globalId'] + compact_fields + ['callId','clientSessionId']

    response = api_get(
        path=f"{get_priv_path(record_type, record_global_id)}/ActivityLog",
    )
    
    result = read_pd(response['data'], out_format)
    result.rename(columns={'resourceUniqueString': 'resourceName'}, inplace=True)

    # Unordered fields will be at end. Is it worth a utility function?
    unordered_fields = set(result.columns) - set(field_ordering)
    result = result[field_ordering + list(unordered_fields)]
    
    display_cols = get_viewtype_columns(view_type, compact_fields, more_fields)
    print_dataframe(
        result,
        out_format,
        restricted_cols=display_cols
    )
    
