import os
from io import BufferedReader
from typing import BinaryIO, List, Dict

import pandas as pd
# pylint: disable=no-name-in-module
from pandas._libs.parsers import STR_NA_VALUES
from pandas.core.frame import DataFrame
from loguru import logger
from requests.exceptions import HTTPError

from austrakka.utils.exceptions import FailedResponseException
from austrakka.utils.exceptions import UnknownResponseException
from austrakka.utils.misc import logger_wraps
from austrakka.utils.api import call_api
from austrakka.utils.api import call_api_raw
from austrakka.utils.api import call_get_api
from austrakka.utils.api import post
from austrakka.utils.api import RESPONSE_TYPE_ERROR
from austrakka.utils.paths import SEQUENCE_PATH
from austrakka.utils.paths import SEQUENCE_BY_SPECIES_PATH
from austrakka.utils.paths import SEQUENCE_BY_GROUP_PATH
from austrakka.utils.paths import SEQUENCE_BY_ANALYSIS_PATH
from austrakka.utils.output import create_response_object
from austrakka.utils.output import log_response
from austrakka.utils.output import log_response_compact
from austrakka.utils.fs import create_dir
from austrakka.utils.enums.seq import FASTA_UPLOAD_TYPE
from austrakka.utils.enums.seq import FASTQ_UPLOAD_TYPE
from austrakka.utils.enums.seq import READ_BOTH
from austrakka.utils.output import print_table

FASTA_PATH = 'Fasta'
FASTQ_PATH = 'Fastq'
DOWNLOAD = 'download'

FASTQ_CSV_SAMPLE_ID = 'Seq_ID'
FASTQ_CSV_SAMPLE_ID_API = 'sample-id'
FASTQ_CSV_PATH_1 = 'filepath1'
FASTQ_CSV_PATH_2 = 'filepath2'
FASTQ_CSV_PATH_1_API = 'filename1'
FASTQ_CSV_PATH_2_API = 'filename2'

FASTA_CSV_SAMPLE = 'SampleId'
FASTA_CSV_FILENAME = 'FileName'
FASTA_CSV_FASTA_ID = 'FastaId'


@logger_wraps()
def add_fasta_submission(csv: BufferedReader):
    usecols = [
        FASTA_CSV_SAMPLE,
        FASTA_CSV_FILENAME,
        FASTA_CSV_FASTA_ID
    ]
    csv_dataframe = _get_and_validate_csv(csv, usecols)

    messages = _validate_fasta_submission(csv_dataframe)
    if messages:
        raise FailedResponseException(messages)

    body = [
        _get_file(filepath) for filepath in csv_dataframe[FASTA_CSV_FILENAME]
    ]
    csv.seek(0)
    body.append(('files[]', (csv.name, csv)))

    call_api(
        method=post,
        path="/".join([SEQUENCE_PATH, FASTA_PATH]),
        body=body,
        multipart=True,
    )


def _validate_fasta_submission(csv_dataframe: DataFrame):
    messages = []

    for _, row in csv_dataframe.iterrows():
        if not os.path.isfile(row[FASTA_CSV_FILENAME]):
            messages.append(create_response_object(
                f'File {row[FASTA_CSV_FILENAME]} not found',
                RESPONSE_TYPE_ERROR
            ))

    return messages


def _get_and_validate_csv(csv: BufferedReader, usecols: List[str]):
    try:
        csv_dataframe = pd.read_csv(
            csv,
            usecols=usecols,
            dtype=str
        )
        return csv_dataframe
    except ValueError:
        logger.error(
            "The CSV file mapping samples to sequences must contain exactly "
            f"the column headers {','.join(usecols)}")
        raise


def _fastq_file_2_is_present(row: pd.Series) -> bool:
    return str(row[FASTQ_CSV_PATH_2]) not in STR_NA_VALUES


def _get_file(filepath: str) -> tuple[str, tuple[str, BinaryIO]]:
    # pylint: disable=consider-using-with
    file = open(filepath, 'rb')
    return 'files[]', (os.path.basename(file.name), file)


@logger_wraps()
def add_fastq_submission(csv: BufferedReader):
    usecols = [
        FASTQ_CSV_SAMPLE_ID,
        FASTQ_CSV_PATH_1,
        FASTQ_CSV_PATH_2
    ]
    csv_dataframe = _get_and_validate_csv(csv, usecols)

    messages = _validate_fastq_submission(csv_dataframe)
    if messages:
        raise FailedResponseException(messages)

    for _, row in csv_dataframe.iterrows():
        try:
            sample_files = []
            custom_headers = {
                FASTQ_CSV_SAMPLE_ID_API: row[FASTQ_CSV_SAMPLE_ID],
                FASTQ_CSV_PATH_1_API: os.path.basename(row[FASTQ_CSV_PATH_1]),
            }
            sample_files.append(_get_file(row[FASTQ_CSV_PATH_1]))

            if _fastq_file_2_is_present(row):
                custom_headers[FASTQ_CSV_PATH_2_API] \
                    = os.path.basename(row[FASTQ_CSV_PATH_2])
                sample_files.append(_get_file(row[FASTQ_CSV_PATH_2]))

            call_api(
                method=post,
                path="/".join([SEQUENCE_PATH, FASTQ_PATH]),
                body=sample_files,
                multipart=True,
                custom_headers=custom_headers,
            )
        except FailedResponseException as ex:
            logger.error(f'Sample {row[FASTQ_CSV_SAMPLE_ID]} failed upload')
            log_response(ex.parsed_resp)
        except (PermissionError, UnknownResponseException, HTTPError) as ex:
            logger.error(f'Sample {row[FASTQ_CSV_SAMPLE_ID]} failed upload')
            logger.error(ex)
        except Exception as ex:
            raise ex from ex


def take_sample_names(data, filter_prop):
    try:
        # Expecting response with flat sample summary dtos
        fss_dtos = list(data)
        fastq_fss_dtos = filter(lambda fss: fss[filter_prop], fss_dtos)
        samples_map = map(lambda x: x['sampleName'], fastq_fss_dtos)
        samples_names = list(samples_map)
        return samples_names

    except Exception as ex:
        logger.error(
            'Error while fetching sample names for samples '
            'with fastq files attached: ')
        raise ex from ex


def _validate_fastq_submission(csv_dataframe: DataFrame):
    messages = []

    if csv_dataframe[FASTQ_CSV_PATH_1].isnull().values.any():
        messages.append(create_response_object(
            f'{FASTQ_CSV_PATH_1} column contains missing values',
            RESPONSE_TYPE_ERROR
        ))

    if csv_dataframe[FASTQ_CSV_SAMPLE_ID].isnull().values.any():
        messages.append(create_response_object(
            f'{FASTQ_CSV_SAMPLE_ID} column contains missing values',
            RESPONSE_TYPE_ERROR
        ))
    if csv_dataframe[FASTQ_CSV_SAMPLE_ID].dropna().duplicated().any():
        messages.append(create_response_object(
            f'{FASTQ_CSV_SAMPLE_ID} column contains duplicate values',
            RESPONSE_TYPE_ERROR
        ))
    if csv_dataframe[FASTQ_CSV_PATH_1].dropna().duplicated().any():
        messages.append(create_response_object(
            f'{FASTQ_CSV_PATH_1} column contains duplicate values',
            RESPONSE_TYPE_ERROR
        ))
    if csv_dataframe[FASTQ_CSV_PATH_2].dropna().duplicated().any():
        messages.append(create_response_object(
            f'{FASTQ_CSV_PATH_2} column contains duplicate values',
            RESPONSE_TYPE_ERROR
        ))

    for _, row in csv_dataframe.iterrows():
        if not os.path.isfile(row[FASTQ_CSV_PATH_1]):
            messages.append(create_response_object(
                f'File {row[FASTQ_CSV_PATH_1]} not found',
                RESPONSE_TYPE_ERROR
            ))

        if _fastq_file_2_is_present(row) \
                and not os.path.isfile(row[FASTQ_CSV_PATH_2]):
            messages.append(create_response_object(
                f'File {row[FASTQ_CSV_PATH_2]} not found',
                RESPONSE_TYPE_ERROR
            ))

    return messages


def _download_seq_file(file_path, filename, query_path, sample_dir):
    try:
        resp = call_api_raw(
            path=query_path,
            stream=True,
        )

        if not os.path.exists(sample_dir):
            create_dir(sample_dir)

        with open(file_path, 'wb') as file:
            for chunk in resp.iter_content(chunk_size=128):
                file.write(chunk)

        logger.success(f'Downloaded: {filename} To: {file_path}')

    except FailedResponseException as ex:
        log_response_compact(ex.parsed_resp)


def _get_seq_download_path(sample_name: str, read: str, seq_type: str):
    download_path = f'{SEQUENCE_PATH}/{DOWNLOAD}'
    download_path += f'/{FASTQ_PATH}/{sample_name}/{read}' \
        if seq_type == FASTQ_UPLOAD_TYPE \
        else f'/{FASTA_PATH}/{sample_name}'
    return download_path


def _download_sequences(
        output_dir: str,
        samples_seq_info: list[Dict],
):
    for ssi in samples_seq_info:
        sample_name = ssi['sampleName']
        dto_read = str(ssi['read'])
        filename = ssi['fileName']
        seq_type = ssi['type']

        sample_dir = os.path.join(output_dir, sample_name)
        file_path = os.path.join(sample_dir, filename)

        if os.path.exists(file_path):
            logger.warning(
                f'Found a local copy of {filename}.  Skipping...')
            continue

        query_path = _get_seq_download_path(sample_name, dto_read, seq_type)
        _download_seq_file(file_path, filename, query_path, sample_dir)


def _filter_sequences(data, seq_type, read) -> List[Dict]:
    data = filter(lambda x: x['type'] == seq_type or seq_type is None, data)
    if seq_type == FASTA_UPLOAD_TYPE:
        return list(data)
    data = filter(lambda x: read == READ_BOTH or x['read'] == int(read), data)
    return list(data)


def _get_seq_api(
        species: str,
        group_name: str,
        analysis: str,
):
    api_path = SEQUENCE_PATH
    if species is not None:
        api_path += f'/{SEQUENCE_BY_SPECIES_PATH}/{species}'
    elif group_name is not None:
        api_path += f'/{SEQUENCE_BY_GROUP_PATH}/{group_name}'
    elif analysis is not None:
        api_path += f'/{SEQUENCE_BY_ANALYSIS_PATH}/{analysis}'
    else:
        raise ValueError("A filter has not been passed")
    return api_path


# pylint: disable=duplicate-code
def _get_seq_data(
        seq_type: str,
        read: str,
        species: str,
        group_name: str,
        analysis: str,
):
    api_path = _get_seq_api(species, group_name, analysis)
    data = call_get_api(path=api_path)
    return _filter_sequences(data, seq_type, read)


# pylint: disable=duplicate-code
def get_sequences(
        output_dir,
        seq_type: str,
        read: str,
        species: str,
        group_name: str,
        analysis: str,
):
    if not os.path.exists(output_dir):
        create_dir(output_dir)

    data = _get_seq_data(
        seq_type,
        read,
        species,
        group_name,
        analysis,
    )
    _download_sequences(output_dir, data)


# pylint: disable=duplicate-code
def list_sequences(
        out_format: str,
        seq_type: str,
        read: str,
        species: str,
        group_name: str,
        analysis: str,
):
    data = _get_seq_data(
        seq_type,
        read,
        species,
        group_name,
        analysis,
    )
    print_table(
        pd.DataFrame(data),
        out_format,
    )
