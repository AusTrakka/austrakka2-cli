import pandas as pd

from austrakka.utils.api import call_api
from austrakka.utils.api import get
from austrakka.utils.misc import logger_wraps
from austrakka.utils.output import print_table
from austrakka.utils.paths import ORG_PATH
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
