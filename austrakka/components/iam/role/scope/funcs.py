from austrakka.utils.api import api_patch
from austrakka.utils.misc import logger_wraps
from austrakka.utils.paths import ROLES_V2_PATH

@logger_wraps()
def add_role_scope(role: str, global_ids: list[str]):
    """
    Add a new scope to a role.
    """
    api_patch(
        path=f"{ROLES_V2_PATH}/{role}/Scope/Add",
        data=global_ids,
    )


@logger_wraps()
def remove_role_scope(role: str, global_ids: list[str]):
    """
    Remove scope from a role.
    """
    api_patch(
        path=f"{ROLES_V2_PATH}/{role}/Scope/Remove",
        data=global_ids,
    )
