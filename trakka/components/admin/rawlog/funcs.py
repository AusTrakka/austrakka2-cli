
from loguru import logger

from trakka.utils.datetimes import dt_parse
from trakka.utils.helpers.output import call_get_and_print
from trakka.utils.api import api_post, api_get
from trakka.utils.misc import logger_wraps
from trakka.utils.output import get_viewtype_columns
from trakka.utils.paths import TENANT_PATH

@logger_wraps()
def show_raw_log(global_id: str, out_format: str):
    '''
    Get a single raw log by global ID.
    '''
    call_get_and_print(
        f"{TENANT_PATH}/RawLog/{global_id}",
        out_format,
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
    api_post(
        f"{TENANT_PATH}/RawLog/{global_id}/Regenerate",
        data={'rawLogGlobalId': global_id}
    )

@logger_wraps()
def regenerate_raw_log_bulk(spec: str, start: str, end: str, submitter: str, 
                            allow_no_filters: bool):
    params = { "allowNoFilters": str(allow_no_filters).lower() }
    if spec is not None:
        params["spec"] = spec
    if start is not None:
        params["startDateTime"] = dt_parse(start)
    if end is not None:
        params["endDateTime"] = dt_parse(end)
    if submitter is not None:
        params["submitterGlobalId"] = submitter

    # First query to check what we are about to do
    # For now we only care about the log count, but in the future may check log status
    logs_response = api_get(
        path=f"{TENANT_PATH}/RawLogs/Metrics",
        params=params,
    )['data']
    
    log_count = logs_response['count']
    if log_count == 0:
        logger.info("No raw logs found matching the specified filters.")
        return
    
    confirmation = input(f"{log_count} raw logs will be regenerated. Do you want to proceed?"
                         " (only yes will continue): ")
    
    if confirmation.lower() != "yes":
        logger.info("Aborting")
        return

    api_post(
        f"{TENANT_PATH}/RawLogs/BulkRegenerate",
        params=params,
    )
