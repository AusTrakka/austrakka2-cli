
from austrakka.utils.helpers.output import call_get_and_print
from austrakka.utils.api import api_post
from austrakka.utils.output import get_viewtype_columns
from austrakka.utils.paths import TENANT_PATH

def show_raw_log(global_id: str, out_format: str, timezone: str):
    '''
    Get a single raw log by global ID.
    '''
    call_get_and_print(
        f"{TENANT_PATH}/RawLog/{global_id}",
        out_format,
        timezone=timezone,
    )

def list_raw_logs(spec: str, start: str, end: str, submitter: str, allow_no_filters: bool,
                  out_format: str, view_type: str, timezone: str):
    '''
    Get a list of raw log entries.
    '''
    # Default tabular columns: all except data
    compact_fields = [
        "globalId","submitterGlobalId","clientSessionId","eventTime","eventStatus","spec",
        "logStatus","callId"
    ]
    
    params = { "allowNoFilters": str(allow_no_filters).lower() }
    if spec is not None:
        params["spec"] = spec
    if start is not None:
        params["startDateTime"] = start
    if end is not None:
        params["endDateTime"] = end
    if submitter is not None:
        params["submitterGlobalId"] = submitter
    
    columns = get_viewtype_columns(view_type, compact_fields, [])
    call_get_and_print(
        f"{TENANT_PATH}/RawLogs",
        out_format,
        params=params,
        restricted_cols=columns,
        timezone=timezone,
    )

def regenerate_raw_log(global_id: str):
    '''
    Regenerate a raw log entry by global ID.
    '''
    # pylint: disable=fixme
    # TODO this path should really be RawLog/{id}/Regenerate, but the API needs updating
    api_post(
        f"{TENANT_PATH}/RawLog/Regenerate/{global_id}",
        data={'rawLogGlobalId': global_id}
    )
