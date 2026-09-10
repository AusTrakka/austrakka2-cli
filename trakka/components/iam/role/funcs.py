from trakka.utils.helpers.output import call_get_and_print
from trakka.utils.output import get_viewtype_columns
from trakka.utils.paths import ROLES_V2_PATH
from trakka.utils.api import api_post, api_patch, api_delete

from trakka.utils.misc import logger_wraps

list_compact_fields = ['name', 'description', 'resourceType', 'privilegeLevel']
list_more_fields = [
    'created', 
    'createdBy']


# pylint: disable=duplicate-code
@logger_wraps()
def list_roles(view_type: str, out_format: str):
    """
    Get the list of roles
    """
    columns = get_viewtype_columns(view_type, list_compact_fields, list_more_fields)
    call_get_and_print(
        ROLES_V2_PATH, 
        out_format, 
        restricted_cols=columns
    )


@logger_wraps()
def add_role(
        role: str, 
        description: str, 
        privilege_level: str, 
        resource_type: str,
        scopes: list[str],
):
    """
    Add a new role
    """
    # switch statement to map string name to integer value
    payload = {
        "name": role,
        "description": description,
        "privilegeLevel": privilege_level,
        "resourceType": resource_type,
        "scopes": list(scopes),
    }

    api_post(
        path=ROLES_V2_PATH,
        data=payload,
    )


@logger_wraps()
def update_role(
        role: str,
        new_name: str,
        description: str,
        privilege_level: str,
        resource_type: str):
    """
    Update a role.
    """
    if (not new_name and
            not description and
            not privilege_level and
            not resource_type):
        raise ValueError("At least one of new_name, description, privilege_level, "
                         "or resource_type must be provided")

    payload = {}
    if new_name:
        payload["name"] = new_name

    if description:
        payload["description"] = description

    if privilege_level:
        payload["privilegeLevel"] = privilege_level

    if resource_type:
        payload["resourceType"] = resource_type

    api_patch(
        path=f"{ROLES_V2_PATH}/{role}",
        data=payload,
    )


@logger_wraps()
def delete_role(role: str):
    """
    Delete a role
    """
    api_delete(
        path=f"{ROLES_V2_PATH}/{role}",
    )
