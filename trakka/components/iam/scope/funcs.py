from trakka.utils.helpers.output import call_get_and_print
from trakka.utils.output import get_viewtype_columns
from trakka.utils.misc import logger_wraps
from trakka.utils.paths import SCOPES_PATH

list_compact_fields = [
    'name', 
    'privilegeLevel', 
    'resourceType']

list_more_fields = [
    'name', 
    'privilegeLevel', 
    'resourceType', 
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
