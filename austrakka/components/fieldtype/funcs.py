from austrakka.utils.misc import logger_wraps
from austrakka.utils.paths import METADATACOLUMNTYPE_PATH
from austrakka.utils.helpers.list import print_get


@logger_wraps()
def list_fieldtypes(table_format: str):
    print_get(METADATACOLUMNTYPE_PATH, table_format)
