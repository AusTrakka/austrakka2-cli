import click

def analysis(func):
    return click.option(
        '-a',
        '--analysis',
        required=True,
        help='Analysis ID',
        type=click.INT
    )(func)
