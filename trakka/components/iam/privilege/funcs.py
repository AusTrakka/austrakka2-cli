from trakka.utils.helpers.output import call_get_and_print

from trakka.utils.api import api_delete, api_post
from trakka.utils.misc import logger_wraps

from trakka.utils.paths import PRIVILEGE_PATH


"""
These functions call PrivilegeController endpoints.
"""

@logger_wraps()
def list_privileges(resource_type, resource_id, user_id, role, out_format):
    """
    List privilege assignments across resources, users, and roles.
    """
    # If resource_id is specified, resource_type must be specified
    if resource_id and not resource_type:
        raise ValueError("Resource type must be specified if resource ID is specified")
    params = dict()
    if resource_type:
        params['resourceTypeFilter'] = resource_type
    if resource_id:
        params['resourceIdentifierFilter'] = resource_id
    if user_id:
        params['assigneeIdentifierFilter'] = user_id
    if role:
        params['roleIdentifierFilter'] = role
    call_get_and_print(PRIVILEGE_PATH, out_format, params=params)
