import click

def species(func):
    return click.option(
        '-s',
        '--species',
        required=True,
        help='Species ID',
        type=click.INT
    )(func)
