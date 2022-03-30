import click


def species(func):
    return click.option(
        '-s',
        '--species',
        required=True,
        help='Species ID',
        type=click.INT
    )(func)


def csv(help_text='CSV file'):
    def inner_func(func):
        return click.option(
            "--csv",
            "csv_file",
            type=click.File('rb'),
            default=None,
            help=help_text
        )(func)

    return inner_func
