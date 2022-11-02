from austrakka.utils.misc import logger_wraps
from austrakka.utils.paths import JOB_INSTANCE_PATH
from austrakka.utils.paths import ANALYSIS_HISTORY_PATH
from austrakka.utils.helpers.output import call_get_and_print_table


@logger_wraps()
def list_instances(out_format: str):
    call_get_and_print_table(
        f'{JOB_INSTANCE_PATH}/{ANALYSIS_HISTORY_PATH}',
        out_format,
    )
