from trakka.utils.helpers.output import call_get_and_print
from trakka.utils.privilege import get_priv_path

from trakka.utils.api import api_delete, api_post
from trakka.utils.misc import logger_wraps


@logger_wraps()
def list_privileges(record_type: str, record_id: str, out_format: str):
    """
    List the privileges assigned to a record.
    """
    call_get_and_print(f"{get_priv_path(record_type, record_id)}/privilege", out_format)


@logger_wraps()
def list_by_role_privileges(role: str, record_type: str, record_id: str, out_format: str):
    """
    List by role the privileges assigned to a record.
    """
    call_get_and_print(
        f"{get_priv_path(record_type, record_id)}/privilege/role/{role}",
        out_format,
    )

@logger_wraps()
def list_by_user_privileges(user_id: str, record_type: str, record_id: str, out_format: str):
    """
    List by user the privileges assigned to a record.
    """
    call_get_and_print(
        f"{get_priv_path(record_type, record_id)}/privilege/user/{user_id}",
        out_format,
    )


@logger_wraps()
def assign_privilege(
        user_id: str,
        role: str,
        record_id: str,
        record_type: str
):
    payload = {
        "roleGlobalId": role,
        "assigneeGlobalId": user_id
    }

    return api_post(
        path=f"{get_priv_path(record_type, record_id)}/privilege",
        data=payload,
    )


@logger_wraps()
def unassign_privilege(
        user_id: str,
        role: str,
        record_id: str,
        record_type: str
):
    api_delete(
        path=f"{get_priv_path(record_type, record_id)}/privilege",
        custom_headers={},
        params = {
            'roleIdentifier': role,
            'userIdentifier': user_id,
        },
    )
