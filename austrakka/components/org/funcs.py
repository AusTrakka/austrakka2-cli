from austrakka.utils.api import api_post
from austrakka.utils.api import api_put
from austrakka.utils.misc import logger_wraps
from austrakka.utils.paths import ORG_PATH
from austrakka.utils.helpers.orgs import get_org_by_abbrev
from austrakka.utils.helpers.output import call_get_and_print


@logger_wraps()
def list_orgs(out_format: str):
    call_get_and_print(ORG_PATH, out_format)


# pylint: disable=duplicate-code
@logger_wraps()
def add_org(
        name: str,
        abbrev: str,
        country: str,
        state: str,
        is_active: bool,
):
    api_post(
        path=ORG_PATH,
        data={
            "Name": name,
            "Abbreviation": abbrev,
            "Country": country,
            "State": state,
            "IsActive": is_active,
        }
    )


# pylint: disable=duplicate-code
@logger_wraps()
def update_org(
        abbrev: str,
        name: str,
        country: str,
        state: str,
        is_active: bool,
):
    org = get_org_by_abbrev(abbrev)

    put_org = {k: org[k] for k in [
        "name",
        "country",
        "state",
        "isActive",
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

    api_put(
        path=f'{ORG_PATH}/{abbrev}',
        data=put_org
    )
