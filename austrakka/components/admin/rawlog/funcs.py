from austrakka.utils.datetimes import dt_parse
from austrakka.utils.helpers.output import call_get_and_print
from austrakka.utils.api import api_post
from austrakka.utils.misc import logger_wraps
from austrakka.utils.output import get_viewtype_columns
from austrakka.utils.paths import TENANT_PATH

@logger_wraps()
def show_raw_log(global_id: str, out_format: str, timezone: str):
    '''
    Get a single raw log by global ID.
    '''
    call_get_and_print(
        f"{TENANT_PATH}/RawLog/{global_id}",
        out_format,
        timezone=timezone,
    )

@logger_wraps()
def list_raw_logs(spec: str, start: str, end: str, submitter: str, allow_no_filters: bool,
                  out_format: str, view_type: str):
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
        params["startDateTime"] = dt_parse(start)
    if end is not None:
        params["endDateTime"] = dt_parse(end)
    if submitter is not None:
        params["submitterGlobalId"] = submitter
    
    columns = get_viewtype_columns(view_type, compact_fields, [])
    call_get_and_print(
        f"{TENANT_PATH}/RawLogs",
        out_format,
        params=params,
        restricted_cols=columns,
    )

@logger_wraps()
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
