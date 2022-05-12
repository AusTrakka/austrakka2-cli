import click
from austrakka.utils.enums.seq import FASTQ_UPLOAD_TYPE
from austrakka.utils.enums.seq import FASTA_UPLOAD_TYPE


def opt_species(func):
    return click.option(
        '-s',
        '--species',
        required=True,
        help='Species Abbreviation',
        type=click.STRING
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
        "-t",
        '--type',
        'seq_type',
        required=True,
        type=click.Choice([FASTA_UPLOAD_TYPE, FASTQ_UPLOAD_TYPE]),
        help='Sequence format',
    )(func)


def opt_output_dir(func):
    return click.option(
        "-o",
        '--outdir',
        'output_dir',
        required=True,
        type=click.Path(exists=False),
        help='The output directory where files are saved. Sub \
        directories will be created beneath this as needed.',
    )(func)


def opt_read(func):
    return click.option(
        "-r",
        '--read',
        'read',
        default="-1",
        type=click.Choice(["-1", "1", "2"]),
        help='Fastq read. Defaults to -1, meaning both 1 and 2',
    )(func)


def opt_analysis(func):
    return click.option(
        '-a',
        '--analysis',
        required=True,
        help='Analysis Abbreviation',
        type=click.STRING
    )(func)
