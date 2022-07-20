from austrakka.utils.misc import logger_wraps
from austrakka.utils.paths import ANALYSIS_PATH
from austrakka.utils.api import call_get_and_print_table


@logger_wraps()
def list_analyses(table_format: str):
    call_get_and_print_table(ANALYSIS_PATH, table_format)
