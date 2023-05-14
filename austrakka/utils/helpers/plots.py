from austrakka.utils.api import api_get
from austrakka.utils.paths import PLOT_PATH


def get_plot_by_abbrev(abbrev: str):
    return api_get(path=f"{PLOT_PATH}/abbrev/{abbrev}")['data']
