from austrakka.utils.helpers.output import call_get_and_print_view_type
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
    call_get_and_print_view_type(
        SCOPES_PATH, 
        view_type, 
        list_compact_fields, 
        list_more_fields,
        out_format, 
    )
