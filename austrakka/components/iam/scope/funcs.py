from austrakka.utils.api import api_get
from austrakka.utils.helpers.tenant import get_default_tenant_global_id
from austrakka.utils.misc import logger_wraps
from austrakka.utils.output import print_response

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
    Get the list of scopes defined for a tenant.
    """
    tenant_global_id = get_default_tenant_global_id()
    response = api_get(path=f"v2/tenant/{tenant_global_id}/scope")
    
    print_response(
        response,
        view_type,
        list_compact_fields,
        list_more_fields,
        out_format,
    )
