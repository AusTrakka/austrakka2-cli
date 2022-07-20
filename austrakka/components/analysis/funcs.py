from austrakka.utils.misc import logger_wraps
from austrakka.utils.paths import ANALYSIS_PATH
from austrakka.utils.helpers.list import print_get


@logger_wraps()
def list_analyses(table_format: str):
    print_get(ANALYSIS_PATH, table_format)
