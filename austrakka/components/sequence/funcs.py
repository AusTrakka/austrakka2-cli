import os
from io import BufferedReader
from typing import BinaryIO, List
from os import path

import pandas as pd
# pylint: disable=no-name-in-module
from pandas._libs.parsers import STR_NA_VALUES
from pandas.core.frame import DataFrame
from loguru import logger

from austrakka.utils.exceptions import FailedResponseException
from austrakka.utils.misc import logger_wraps
from austrakka.utils.api import call_api
from austrakka.utils.api import call_api_raw
from austrakka.utils.api import call_get_api
from austrakka.utils.api import post
from austrakka.utils.api import RESPONSE_TYPE_ERROR
from austrakka.utils.paths import SEQUENCE_PATH
from austrakka.utils.paths import SAMPLE_BY_SPECIES_PATH
from austrakka.utils.paths import SAMPLE_DOWNLOAD_INFO_PATH
from austrakka.utils.output import create_response_object
from austrakka.utils.output import log_response
from austrakka.utils.output import log_response_compact
from austrakka.utils.fs import create_dir
from austrakka.utils.enums.seq import FASTA_UPLOAD_TYPE
from austrakka.utils.enums.seq import FASTQ_UPLOAD_TYPE

FASTA_PATH = 'Fasta'
FASTQ_PATH = 'Fastq'
DOWNLOAD = 'download'

ALL_READS = "-1"
ONE = "1"
TWO = "2"

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
        except PermissionError as ex:
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


def download_fastq_for_each_sample(
    output_dir: str,
    samples_seq_info: list[tuple[any, any]],
    read: str
):
    for ssi in samples_seq_info:
        sample_name = ssi[0]

        for seq_dto in ssi[1]:
            dto_read = str(seq_dto['read'])
            seq_type = seq_dto['type']

            if not sample_name:
                logger.error('Encountered empty sample name. Skipping all '
                             'sequences associated with the sample...')
                continue

            if dto_read not in (ONE, TWO) or not seq_type:
                logger.error(f'Error in sample: {sample_name}. Found sequence '
                             f'with invalid Read or Type. Skipping...')
                continue

            # When read is -1, it means take both.
            # Ignore fasta. Some samples can have both fasta and fastq files.
            if seq_type.lower() == FASTA_UPLOAD_TYPE \
                    or read not in (dto_read, ALL_READS):
                continue

            filename = seq_dto['fileName']
            sample_dir = os.path.join(output_dir, sample_name)
            file_path = os.path.join(sample_dir, filename)

            if os.path.exists(file_path):
                logger.warning(
                    f'Found a local copy of {filename}.  Skipping...')
                continue

            query_path = path.join(
                SEQUENCE_PATH,
                DOWNLOAD,
                FASTQ_PATH,
                sample_name,
                dto_read,
            )
            download_seq_file(file_path, filename, query_path, sample_dir)


def download_fasta_for_each_sample(
    output_dir: str,
    samples_seq_info: list[tuple[any, any]]
):
    for ssi in samples_seq_info:
        sample_name = ssi[0]

        for seq_dto in ssi[1]:
            seq_type = seq_dto['type']

            if not sample_name:
                logger.error('Encountered empty sample name. Skipping all '
                             'sequences associated with the sample...')
                continue

            if seq_type.lower() == FASTQ_UPLOAD_TYPE:
                continue

            filename = seq_dto['fileName']
            sample_dir = os.path.join(output_dir, sample_name)
            file_path = os.path.join(sample_dir, filename)

            if os.path.exists(file_path):
                logger.warning(
                    f'Found a local copy of {filename}.  Skipping...')
                continue

            query_path = path.join(
                SEQUENCE_PATH,
                DOWNLOAD,
                FASTA_PATH,
                sample_name,
            )
            download_seq_file(file_path, filename, query_path, sample_dir)


def download_seq_file(file_path, filename, query_path, sample_dir):
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


def fetch_seq_download_info(sample_names):
    samples_seq_info = []
    for name in sample_names:
        info = call_get_api(
            path=path.join(SAMPLE_DOWNLOAD_INFO_PATH, name),
        )
        samples_seq_info.append((name, info))
    return samples_seq_info


def throw_if_empty(a_list: list, msg: str):
    if not a_list:
        raise FailedResponseException(
            create_response_object(
                msg, RESPONSE_TYPE_ERROR))


def fetch_samples_names_by_species(species: str):
    samples = call_get_api(
        path=path.join(SAMPLE_BY_SPECIES_PATH, species),
    )
    return samples
