import pandas as pd
from loguru import logger

from typing import List

from austrakka.utils.api import call_api
from austrakka.utils.api import get, post
from austrakka.utils.misc import logger_wraps
from austrakka.utils.output import print_table
from austrakka.utils.paths import PROFORMA_PATH

@logger_wraps()
def add_proforma(
        abbrev: str, 
        name: str, 
        description: str, 
        suggested_species: List[str],
        required_columns: List[str],
        optional_columns: List[str]):
        
    # TODO: check that all system fields are included (or let endpoint take care of it?)
    columnNames = ([{"name": col, "isRequired": True} for col in required_columns] 
                    + [{"name": col, "isRequired": False} for col in optional_columns])
    if len(columnNames)==0:
        raise ValueError("A pro forma must contain at least one field")
    return call_api(
        method=post,
        path=PROFORMA_PATH,
        body={
            "abbreviation": abbrev,
            "name": name,
            "description": description,
            "speciesAbbrev": suggested_species,
            "columnNames": columnNames  
        })
       

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

    result.drop(['columnMappings',
                 'proFormaVersionId',
                 'lastUpdatedBy',
                 'lastUpdated'],
                axis='columns',
                inplace=True)

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

    for field in ['abbreviation', 'name', 'version', 'description']:
        logger.info(f'{field}: {data[field]}')

    species_field = 'suggestedSpecies'
    species = ','.join([s['abbrev'] for s in data[species_field]])
    logger.info(f'{species_field}: {species}')

    logger.info('Pro forma fields:')

    # Should add isActive check, but probably in endpoint
    field_df = pd.DataFrame.from_dict(data['columnMappings'])[
        ['metaDataColumnName', 'metaDataColumnPrimitiveType', 'isRequired']]

    field_df.rename(
        columns={'metaDataColumnPrimitiveType': 'type'},
        inplace=True
    )

    field_df['type'].fillna('categorical', inplace=True)
    print_table(
        field_df,
        table_format,
    )
