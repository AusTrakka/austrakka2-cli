from austrakka.utils.api import call_api, put
from austrakka.utils.helpers.output import call_get_and_print_table
from austrakka.utils.api import post
from austrakka.utils.paths import SPECIES_PATH
from austrakka.utils.misc import logger_wraps
from austrakka.utils.helpers.species import get_species_by_abbrev


@logger_wraps()
def add_species(abbrev: str, name: str, taxon_id: str, is_active: bool):
    return call_api(
        method=post,
        path=SPECIES_PATH,
        body={
            "abbreviation": abbrev,
            "name": name,
            "taxonId": taxon_id,
            "isActive": is_active,
        }
    )


@logger_wraps()
def list_species(out_format: str):
    call_get_and_print_table(SPECIES_PATH, out_format)


@logger_wraps()
def update_species(abbrev: str, name: str, taxon_id: str, is_active: bool):
    species = get_species_by_abbrev(abbrev)

    if name is not None:
        species['name'] = name

    if taxon_id is not None:
        species['taxonId'] = taxon_id

    if is_active is not None:
        species['isActive'] = is_active

    return call_api(
        method=put,
        path=f'{SPECIES_PATH}/{species["abbreviation"]}',
        body=species
    )
