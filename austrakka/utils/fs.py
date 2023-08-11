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
    for uploadDto in resp['data']:
        if not any(
                f.filename == uploadDto['originalFileName']
                and f.sha256.casefold() == uploadDto['serverSha256'].casefold()
                for f in hashes
        ):
            errors.append(f'Hash for {uploadDto["originalFileName"]} is not correct')
    if any(errors):
        raise IncorrectHashException(", ".join(errors))


def verify_hash_single(a_hash: FileHash, resp: dict):
    errors = []
    upload_dto = resp['data']

    if not (
            a_hash.filename == upload_dto['originalFileName'] and
            a_hash.sha256.casefold() == upload_dto['serverSha256'].casefold()
    ):
        errors.append(f'Hash for {upload_dto["originalFileName"]} is not correct')

    if any(errors):
        raise IncorrectHashException(", ".join(errors))
