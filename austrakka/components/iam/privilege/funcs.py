from austrakka.utils.helpers.output import call_get_and_print
from austrakka.utils.privilege import get_priv_path
from austrakka.utils.subcommands.shared_funcs import (
    get_role_global_id_by_name)

from austrakka.utils.api import api_delete, api_post
from austrakka.utils.misc import logger_wraps


@logger_wraps()
def list_privileges(record_type: str, record_global_id: str, out_format: str):
    """
    List the privileges assigned to a record.
    """
    call_get_and_print(f"{get_priv_path(record_type, record_global_id)}/privilege", out_format)


@logger_wraps()
def list_by_role_privileges(role: str, record_type: str, record_global_id: str, out_format: str):
    """
    List by role the privileges assigned to a record.
    """
    role_global_id = get_role_global_id_by_name(role)
    call_get_and_print(
        f"{get_priv_path(record_type, record_global_id)}/privilege/role/{role_global_id}",
        out_format,
    )

@logger_wraps()
def list_by_user_privileges(user_id: str, record_type: str, record_global_id: str, out_format: str):
    """
    List by user the privileges assigned to a record.
    """
    call_get_and_print(
        f"{get_priv_path(record_type, record_global_id)}/privilege/user/{user_id}",
        out_format,
    )


@logger_wraps()
def assign_privilege(
        user_global_id: str,
        role: str,
        record_global_id: str,
        record_type: str
):
    payload = {
        "roleGlobalId": get_role_global_id_by_name(role),
        "assigneeGlobalId": user_global_id
    }

    return api_post(
        path=f"{get_priv_path(record_type, record_global_id)}/privilege",
        data=payload,
    )


@logger_wraps()
def unassign_privilege(
        record_global_id: str,
        record_type: str,
        privilege_global_id: str
):
    api_delete(
        path=f"{get_priv_path(record_type, record_global_id)}/privilege/{privilege_global_id}",
        custom_headers={}
    )
