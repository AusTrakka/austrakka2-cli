from austrakka.utils.helpers.output import call_get_and_print_view_type
from austrakka.utils.paths import ROLES_V2_PATH, ROOT_TYPES_PATH
from austrakka.utils.subcommands.shared_funcs import get_role_by_name, get_role_global_id_by_name
from austrakka.utils.api import api_get, api_post, api_patch, api_delete
from austrakka.utils.enums.privilege_level import (
    AUSTRAKKA_ADMIN_LEVEL,
    FUNCTIONAL_ADMIN_LEVEL,
    USER_LEVEL)

from austrakka.utils.misc import logger_wraps

list_compact_fields = ['name', 'description', 'privilegeLevel', 'globalId']
list_more_fields = [
    'name', 
    'description', 
    'privilegeLevel', 
    'allowedRootTypes', 
    'globalId', 
    'created', 
    'createdBy']


# pylint: disable=duplicate-code
@logger_wraps()
def list_roles(view_type: str, out_format: str):
    """
    Get the list of roles
    """
    call_get_and_print_view_type(
        ROLES_V2_PATH, 
        view_type, 
        list_compact_fields, 
        list_more_fields,
        out_format, 
    )


@logger_wraps()
def add_role(role: str, description: str, privilege_level: str, allowed_record_types: list[str]):
    """
    Add a new role
    """
    # switch statement to map string name to integer value
    level = _privilege_name_to_int()
    payload = {
        "name": role,
        "description": description,
        "privilegeLevel": level[privilege_level],
    }

    _assign_allowed_role_root_types(allowed_record_types, payload)

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
        level = _privilege_name_to_int()
        payload["privilegeLevel"] = level[privilege_level]

    if not clear_allowed_record_types and allowed_record_types:
        _assign_allowed_role_root_types(allowed_record_types, payload)

    if clear_allowed_record_types:
        payload["AllowedRootTypeGlobalIds"] = []

    api_patch(
        path=f"{ROLES_V2_PATH}/{get_role_global_id_by_name(role)}",
        data=payload,
    )


def _assign_allowed_role_root_types(allowed_record_types, payload):
    root_types = api_get(
        path=ROOT_TYPES_PATH,
    )
    # Match allowed record types to root types by name.
    # Gather the global ID of the root type into a list.
    allowed_record_types_global_ids = []
    for record_type in allowed_record_types:
        
        record_type_obj = next((r for r in root_types['data']
                                if (r['name'] == record_type and
                                    r['isAggregateRoot'] is True)), None)
        
        if record_type_obj is None:
            raise ValueError(f"Record type {record_type} not found")
        
        allowed_record_types_global_ids.append(record_type_obj['globalId'])
        
    if len(allowed_record_types_global_ids) > 0:
        payload["AllowedRootTypeGlobalIds"] = allowed_record_types_global_ids


@logger_wraps()
def delete_role(role: str):
    """
    Delete a role
    """
    role_obj = get_role_by_name(role)
    
    api_delete(
        path=f"{ROLES_V2_PATH}/{role_obj['globalId']}",
    )


def _privilege_name_to_int():
    level = {
        AUSTRAKKA_ADMIN_LEVEL: 10000,
        FUNCTIONAL_ADMIN_LEVEL: 20000,
        USER_LEVEL: 30000,
    }
    return level
