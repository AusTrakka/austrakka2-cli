from austrakka.utils.helpers.output import call_get_and_print
from austrakka.utils.misc import logger_wraps


@logger_wraps()
def get_activity(out_format: str):
    """
    Get the activity log for the platform.
    """
    call_get_and_print(
        path=f"Tenant/ActivityLog",
        out_format=out_format,
    )


@logger_wraps()
def get_activity_by_record_type(
        record_type: str,
        record_global_id: str,
        out_format: str):
    """
    Get the activity log for a specific record type.
    """
    call_get_and_print(
        path=f"{record_type}/{record_global_id}/ActivityLog",
        out_format=out_format,
    )
