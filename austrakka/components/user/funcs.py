from typing import List

import pandas as pd

from austrakka.utils.api import call_api
from austrakka.utils.api import get
from austrakka.utils.api import post
from austrakka.utils.api import put
from austrakka.utils.misc import logger_wraps
from austrakka.utils.output import print_table
from austrakka.utils.paths import USER_PATH
from austrakka.utils.helpers.users import get_user_by_email


def get_users(include_all: bool = False):
    response = call_api(
        method=get,
        path=USER_PATH,
        params={
            'includeall': include_all
        }
    )

    result = pd.DataFrame.from_dict(response)
    return result


@logger_wraps()
def list_users(table_format: str):
    result = get_users()

    print_table(
        result,
        table_format,
    )


@logger_wraps()
def add_user(email: str, org: str, roles: List[str], is_active: bool):
    call_api(
        method=post,
        path=USER_PATH,
        body={
            "userLogin": email,
            "userOrganisation": {
                "abbreviation": org
            },
            "roles": [
                {
                    "name": role
                }
                for role in roles
            ],
            "isActive": is_active,
        }
    )


@logger_wraps()
def update_user(email: str, org: str, roles: List[str], is_active: bool):
    user = get_user_by_email(email)

    print(user)
    if org is not None:
        user["userOrganisation"]["abbreviation"] = org

    if roles is not None and len(roles) > 0:
        user["roles"] = [{"name": role} for role in roles]

    if is_active is not None:
        user["IsActive"] = is_active
    print(user)
    call_api(
        method=put,
        path=f'{USER_PATH}/{user["userId"]}',
        body=user
    )
