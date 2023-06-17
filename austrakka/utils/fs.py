import os
from loguru import logger


def create_dir(output_dir):
    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    except PermissionError as ex:
        raise ValueError(
            f'Write permission denied for given output directory {output_dir}') from ex


def remove_empty_dirs(root_dir, ignore: list):
    for root, dirs, files in os.walk(root_dir, topdown=False):
        for d in dirs:
            candidate = os.path.join(root, d)
            if d not in ignore and len(os.listdir(candidate)) == 0:
                logger.info(f'Deleting empty directory: {candidate}')
                os.rmdir(candidate)
