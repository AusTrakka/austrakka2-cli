import pandas as pd

from austrakka.utils.api import api_get
from austrakka.utils.output import print_dataframe
from austrakka.utils.paths import GROUP_PATH


def get_group_by_name(name: str):
    return api_get(path=f"{GROUP_PATH}/{name}")['data']


def format_group_dto_for_output(data, out_format):
    result = pd.json_normalize(data, max_level=1)

    if 'organisation' in result.columns:
        result.drop(['organisation'],
                    axis='columns',
                    inplace=True)

    result.fillna('', inplace=True)
    print_dataframe(result, out_format)
