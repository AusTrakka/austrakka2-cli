from austrakka.utils.api import api_get
from austrakka.utils.paths import ANALYSIS_PATH


def get_analysis_by_abbrev(abbrev: str):
    response = api_get(
        path=f"{ANALYSIS_PATH}/abbrev/{abbrev}"
    )
    return response['data'] if ('data' in response) else response
