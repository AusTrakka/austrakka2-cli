from trakka.utils.helpers.output import call_get_and_print
from trakka.utils.output import get_viewtype_columns

from trakka.utils.misc import logger_wraps

from trakka.utils.paths import PRIVILEGE_PATH

# These functions call PrivilegeController endpoints

COMPACT_FIELDS = ['username','userDisplayName','role',
                  'resourceType','resourceName','resourceEnabled']
MORE_FIELDS = ['userGlobalId','roleGlobalId','resourceGlobalId']

@logger_wraps()
def list_privileges(resource_type: str,
                    resource_id: str,
                    user_id, role,
                    out_format: str,
                    view_type: str):
    """
    List privilege assignments across resources, users, and roles.
    """
    # If resource_id is specified, resource_type must be specified
    if resource_id and not resource_type:
        raise ValueError("Resource type must be specified if resource ID is specified")
    params = {}
    if resource_type:
        params['resourceTypeFilter'] = resource_type
    if resource_id:
        params['resourceIdentifierFilter'] = resource_id
    if user_id:
        params['assigneeIdentifierFilter'] = user_id
    if role:
        params['roleIdentifierFilter'] = role
    columns = get_viewtype_columns(view_type, COMPACT_FIELDS, MORE_FIELDS)
    call_get_and_print(PRIVILEGE_PATH, out_format, params=params, restricted_cols=columns)
