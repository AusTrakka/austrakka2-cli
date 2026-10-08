from trakka.utils.api import api_post, api_patch
from trakka.utils.api import api_put
from trakka.utils.misc import logger_wraps
from trakka.utils.paths import ORG_PATH
from trakka.utils.helpers.orgs import get_org_by_abbrev
from trakka.utils.helpers.output import call_get_and_print


@logger_wraps()
def list_orgs(out_format: str, show_disabled: bool):
    call_get_and_print(ORG_PATH, out_format, {
        "includeall": show_disabled,
    })


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
        state: str
):
    org = get_org_by_abbrev(abbrev)

    put_org = {k: org[k] for k in [
        "name",
        "country",
        "state",
        "organisationId",
    ]}

    if name is not None:
        put_org["Name"] = name
    if country is not None:
        put_org["Country"] = country
    if state is not None:
        put_org["State"] = state

    api_put(
        path=f'{ORG_PATH}/{abbrev}',
        data=put_org
    )

@logger_wraps()
def disable_org(abbrev: str):
    api_patch(
        path=f'{ORG_PATH}/{abbrev}/disable'
    )

@logger_wraps()
def enable_org(abbrev: str):
    api_patch(
        path=f'{ORG_PATH}/{abbrev}/enable'
    )
