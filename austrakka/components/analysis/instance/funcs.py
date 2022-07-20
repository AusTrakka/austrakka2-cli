from austrakka.utils.misc import logger_wraps
from austrakka.utils.paths import JOB_INSTANCE_PATH
from austrakka.utils.paths import ANALYSIS_HISTORY_PATH
from austrakka.utils.helpers.list import print_get


@logger_wraps()
def list_instances(table_format: str):
    print_get(
        f'{JOB_INSTANCE_PATH}/{ANALYSIS_HISTORY_PATH}',
        table_format,
    )
