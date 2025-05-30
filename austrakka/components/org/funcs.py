from austrakka.utils.api import api_post, api_patch
from austrakka.utils.api import api_put
from austrakka.utils.helpers.tenant import get_default_tenant_global_id
from austrakka.utils.misc import logger_wraps
from austrakka.utils.paths import ORG_PATH, ORG_V2_PATH
from austrakka.utils.helpers.orgs import get_org_by_abbrev
from austrakka.utils.helpers.output import call_get_and_print


SAMPLES_OWNER = 'samplesOwner'


@logger_wraps()
def change_owner(curr_owner: str, new_owner: str, seq_ids: [str]):
    tenant = get_default_tenant_global_id()
    api_patch(
        path="/".join(['v2', ORG_V2_PATH, curr_owner, SAMPLES_OWNER]),
        params={"owningTenantGlobalId": tenant},
        data={
            "seqIds": seq_ids,
            "newOwnerAbbrev": new_owner
        },
    )


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
