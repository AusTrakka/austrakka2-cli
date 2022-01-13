import click


def project(func):
    return click.option(
        '-p',
        '--project',
        required=True,
        help='Project ID',
        type=click.INT
    )(func)
