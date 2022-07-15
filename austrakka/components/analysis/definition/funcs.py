from typing import List

from austrakka.utils.api import call_api, post
from austrakka.utils.paths import JOB_DEFINITION_PATH


def add_definition(
        name: str,
        description: str,
        species: List[str],
        is_active: bool
):
    call_api(
        method=post,
        path=JOB_DEFINITION_PATH,
        body={
            "name": name,
            "description": description,
            "species": [
                {
                    "abbreviation": species_item
                }
                for species_item in species
            ],
            "isActive": is_active,
            "unavailable": True,
        }
    )
