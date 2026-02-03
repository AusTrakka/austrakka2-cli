from austrakka.utils.helpers.output import call_get_and_print
from austrakka.utils.output import get_viewtype_columns
from austrakka.utils.misc import logger_wraps
from austrakka.utils.paths import SCOPES_PATH

list_compact_fields = [
    'scopePath', 
    'shortDescription', 
    'privilegeLevel', 
    'globalId', 
    'subjectRootType']

list_more_fields = [
    'scopePath', 
    'shortDescription', 
    'privilegeLevel', 
    'globalId', 
    'subjectRootType', 
    'description']


# pylint: disable=duplicate-code
@logger_wraps()
def list_scopes(view_type:str, out_format: str):
    """
    Get the list of scopes
    """
    columns = get_viewtype_columns(view_type, list_compact_fields, list_more_fields)
    call_get_and_print(
        SCOPES_PATH, 
        out_format,
        restricted_cols=columns
    )
