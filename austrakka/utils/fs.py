import os

from loguru import logger


def create_dir(output_dir):
    try:
        if not os.path.exists(output_dir):
            # If the file exists, call _get_new_file_path to get an
            # incremented name
            logger.info(f'Directory: {output_dir} does not exist. '
                        f'Creating directory...')
            os.makedirs(output_dir)
    except PermissionError:
        raise ValueError(f'Write permission denied for given output ' +
                         f'directory {output_dir}')


def can_write(output_dir):
    try:
        return os.access(output_dir, os.W_OK)
    except OSError:
        raise ValueError(f'directory {output_dir} doesn\'t exist.')

