import hashlib
import os
from dataclasses import dataclass

from austrakka.utils.exceptions import IncorrectHashException


@dataclass
class FileHash:
    filename: str
    sha256: str


def create_dir(output_dir):
    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    except PermissionError as ex:
        raise ValueError(
            f'Write permission denied for given output directory {output_dir}') from ex


def verify_hash(hashes: list[FileHash], resp: dict):
    errors = []
    for upload_dto in resp['data']:
        if not any(
                f.filename == upload_dto['originalFileName']
                and f.sha256.casefold() == upload_dto['serverSha256'].casefold()
                for f in hashes
        ):
            errors.append(f'Hash for {upload_dto["originalFileName"]} is not correct')
    if any(errors):
        raise IncorrectHashException(", ".join(errors))


def verify_hash_single(a_hash: FileHash, resp: dict):
    error = ''
    upload_dto = resp['data']

    if not (
            a_hash.filename == upload_dto['originalFileName'] and
            a_hash.sha256.casefold() == upload_dto['serverSha256'].casefold()
    ):
        error = f'Hash for {upload_dto["originalFileName"]} is not correct'

    if error != '':
        raise IncorrectHashException(error)


def verify_hash_dataset_job(a_hash: FileHash, upload_dto: dict):
    error = ''

    if not (
            a_hash.sha256.casefold() == upload_dto['serverSha256'].casefold()
    ):
        error = 'Hash for this dataset job is not correct'

    if error != '':
        raise IncorrectHashException(error)


def get_hash(filepath):
    with open(filepath, 'rb') as file:
        return FileHash(
            filename=os.path.basename(filepath),
            sha256=hashlib.sha256(file.read()).hexdigest())
