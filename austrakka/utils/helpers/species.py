from austrakka.utils.api import call_api
from austrakka.utils.api import get
from austrakka.utils.paths import SPECIES_PATH


def get_species_by_abbrev(abbrev: str):
    response = call_api(
        method=get,
        path=f"{SPECIES_PATH}/abbrev/{abbrev}"
    )
    return response['data'] if ('data' in response) else response
