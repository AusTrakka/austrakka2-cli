import pandas as pd

from austrakka.utils.api import call_api
from austrakka.utils.api import get
from austrakka.utils.api import post
from austrakka.utils.api import put
from austrakka.utils.misc import logger_wraps
from austrakka.utils.output import print_table
from austrakka.utils.paths import ORG_PATH
from austrakka.utils.helpers.orgs import get_org_by_id
from austrakka.components.user.funcs import get_users


@logger_wraps()
def list_orgs(table_format: str):
    response = call_api(
        method=get,
        path=ORG_PATH,
        params={
            'includeall': False
        }
    )

    result = pd.DataFrame.from_dict(response)

    users = get_users()
    users.set_index('userID', inplace=True)

    result = result.join(users[['displayName']].rename(
        columns={'displayName': 'createdBy'}), on='createdById')
    result['createdBy'] = result['createdBy'].fillna('unknown')
    result = result.join(users[['displayName']].rename(
        columns={'displayName': 'lastUpdatedBy'}), on='lastUpdatedById')
    result['lastUpdatedBy'] = result['lastUpdatedBy'].fillna('unknown')

    result.drop(['createdById', 'lastUpdatedById'],
                axis='columns', inplace=True)

    print_table(
        result,
        table_format,
    )


@logger_wraps()
def add_org(
    name: str,
    abbrev: str,
    country: str,
    state: str,
    is_active: bool,
):
    call_api(
        method=post,
        path=ORG_PATH,
        body={
            "Name": name,
            "Abbreviation": abbrev,
            "Country": country,
            "State": state,
            "IsActive": is_active,
        }
    )


@logger_wraps()
def update_org(
        identifier: int,
        name: str,
        country: str,
        state: str,
        is_active: bool,
):
    org = get_org_by_id(identifier)

    put_org = {k: org[k] for k in [
        "name",
        "country",
        "state",
        "isActive",
        "abbreviation",
        "organisationId",
    ]}

    if name is not None:
        put_org["Name"] = name
    if country is not None:
        put_org["Country"] = country
    if state is not None:
        put_org["State"] = state
    if is_active is not None:
        put_org["IsActive"] = is_active

    call_api(
        method=put,
        path=f'{ORG_PATH}/{identifier}',
        body=put_org
    )
