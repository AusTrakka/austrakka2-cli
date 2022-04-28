import click
from austrakka.utils.enums.seq import FASTQ_UPLOAD_TYPE
from austrakka.utils.enums.seq import FASTA_UPLOAD_TYPE


def opt_species(func):
    return click.option(
        '-s',
        '--species',
        required=True,
        help='Species ID',
        type=click.INT
    )(func)


def opt_csv(help_text='CSV file'):
    def inner_func(func):
        return click.option(
            "--csv",
            "csv_file",
            type=click.File('rb'),
            default=None,
            help=help_text
        )(func)

    return inner_func


def opt_seq_type(func):
    return click.option(
        '--type',
        'seq_type',
        required=True,
        type=click.Choice([FASTA_UPLOAD_TYPE, FASTQ_UPLOAD_TYPE]),
        help='Sequence format',
    )
