from trakka.utils.helpers.output import call_get_and_print
from trakka.utils.output import get_viewtype_columns
from trakka.utils.paths import ROLES_V2_PATH
from trakka.utils.api import api_post, api_patch, api_delete

from trakka.utils.misc import logger_wraps

list_compact_fields = ['name', 'description', 'privilegeLevel']
list_more_fields = [
    'name', 
    'description', 
    'privilegeLevel', 
    'resourceTypes', 
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
        allowed_record_types: list[str],
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
        "resourceTypes": list(allowed_record_types),
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
        allowed_record_types: list[str],
        clear_allowed_record_types: bool):
    """
    Update a role.
    """
    if (not new_name and
            not description and
            not privilege_level and
            not allowed_record_types and
            not clear_allowed_record_types):
        raise ValueError("At least one of new_name, description, privilege_level, "
                         "clear_allowed_record_types, or allowed_record_types must be provided")

    payload = {}
    if new_name:
        payload["name"] = new_name

    if description:
        payload["description"] = description

    if privilege_level:
        payload["privilegeLevel"] = privilege_level

    if not clear_allowed_record_types and allowed_record_types:
        payload["resourceTypes"] = list(allowed_record_types)

    if clear_allowed_record_types:
        payload["resourceTypes"] = []

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
