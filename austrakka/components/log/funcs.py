from austrakka.utils.helpers.output import call_get_and_print
from austrakka.utils.misc import logger_wraps
from austrakka.utils.privilege import get_priv_path


@logger_wraps()
def list_logs(
        record_type: str,
        record_global_id: str,
        out_format: str):
    call_get_and_print(f"{get_priv_path(record_type, record_global_id)}/ActivityLog", out_format)
