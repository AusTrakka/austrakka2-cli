import pandas as pd

from austrakka.utils.api import call_api
from austrakka.utils.api import get
from austrakka.utils.misc import logger_wraps
from austrakka.utils.output import print_table
from austrakka.utils.paths import PROFORMA_PATH


@logger_wraps()
def list_proformas(table_format: str):
    response = call_api(
        method=get,
        path=PROFORMA_PATH,
        params={
            'includeall': False
        }
    )

    data = response['data']
    result = pd.DataFrame.from_dict(data)

    result['suggestedSpecies'] = result['suggestedSpecies'].apply(
        lambda slist: ','.join([species['abbrev'] for species in slist])
    )

    result.drop(
        ['columnMappings', 'proFormaVersionId', 'lastUpdatedBy', 'lastUpdated'],
        axis='columns',
        inplace=True
    )

    print_table(
        result,
        table_format,
    )


@logger_wraps()
def show_proformas(abbrev: str, table_format: str):
    response = call_api(
        method=get,
        path=f'{PROFORMA_PATH}/abbrev/{abbrev}',
    )
    data = response['data']

    for field in ['abbreviation','name','version','description']:
        print(f'{field}: {data[field]}')

    species_field = 'suggestedSpecies'
    species = ','.join([s['name'] for s in data[species_field]])
    print(f'{species_field}: {species}')

    print('Pro forma fields:')

    # Should add isActive check, but probably in endpoint
    field_df = pd.DataFrame.from_dict(data['columnMappings'])[
        ['metaDataColumnName','metaDataColumnPrimitiveType','isRequired']]

    field_df.rename(
        columns={'metaDataColumnPrimitiveType': 'type'},
        inplace=True
    )

    field_df['type'].fillna('categorical', inplace=True)
    print_table(
            field_df,
            table_format,
        )
