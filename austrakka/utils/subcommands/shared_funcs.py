from austrakka.utils.api import api_get
from austrakka.utils.paths import ROLES_V2_PATH
from austrakka.utils.privilege import get_priv_path


def get_role_by_name(role):
    existing_roles = api_get(
        path=ROLES_V2_PATH,
    )
    role_obj = next((r for r in existing_roles['data'] if r['name'] == role), None)
    return role_obj


def get_role_global_id_by_name(role):
    role = get_role_by_name(role)
    if role is None:
        raise ValueError(f"Role {role} not found")
    return role['globalId']


def get_privileges_by_user(
        user_id: str,
        record_type: str,
        record_global_id: str,
):
    """
    List by user the privileges assigned to a record.
    """
    return api_get(
        path=f"{get_priv_path(record_type, record_global_id)}/privilege/user/{user_id}"
    )
