import os


def create_dir(output_dir):
    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    except PermissionError:
        raise ValueError(f'Write permission denied for given output ' +
                         f'directory {output_dir}')


def can_write(output_dir):
    try:
        return os.access(output_dir, os.W_OK)
    except OSError:
        raise ValueError(f'directory {output_dir} doesn\'t exist.')
