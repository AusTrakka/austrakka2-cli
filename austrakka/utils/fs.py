import os


def create_dir(output_dir):
    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    except PermissionError as ex:
        raise ValueError(
            f'Write permission denied for given output directory {output_dir}') from ex
