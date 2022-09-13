import click
from austrakka.utils.enums.seq import FASTQ_UPLOAD_TYPE
from austrakka.utils.enums.seq import FASTA_UPLOAD_TYPE
from austrakka.utils.enums.roles import get_role_list


def opt_abbrev(
        help_text="Abbreviated name, for use with the CLI and in metadata uploads"):
    def inner_func(func):
        return click.option(
            "-a",
            "--abbrev",
            required=True,
            help=help_text
        )(func)
    return inner_func


def opt_name(help_text='Name', required=True, var_name='name'):
    def inner_func(func):
        return click.option(
            "-n",
            "--name",
            var_name,
            required=required,
            help=help_text
        )(func)
    return inner_func


def opt_description(required=True):
    def inner_func(func):
        return click.option(
            '-d',
            '--description',
            default="",
            help='Human-readable description text',
            type=click.STRING,
            required=required,
        )(func)
    return inner_func


def opt_species(required=True, multiple=False):
    def inner_func(func):
        return click.option(
            '-s',
            '--species',
            required=required,
            help='Species Abbreviation',
            type=click.STRING,
            multiple=multiple,
        )(func)
    return inner_func


def opt_organisation(required=True):
    def inner_func(func):
        return click.option(
            '-o',
            '--org',
            required=required,
            help='Organisation abbreviation. Must match an organisation ' +
            'known to AusTrakka, use `austrakka org list` to see valid values',
            type=click.STRING
        )(func)
    return inner_func


def opt_group(required=True):
    def inner_func(func):
        return click.option(
            '-g',
            '--group-names',
            required=required,
            help='Name of group to be granted access to the proforma. '
                 'Multiple fields may be added.',
            type=click.STRING,
            multiple=True
        )(func)
    return inner_func


def opt_proforma(func):
    return click.option(
        '-p',
        '--proforma',
        required=True,
        help='Proforma abbreviation. Use `austrakka proforma list` '
             + 'to see options.',
        type=click.STRING)(func)


def opt_csv(help_text='CSV file', required=False):
    def inner_func(func):
        return click.option(
            "--csv",
            "csv_file",
            type=click.File('rb'),
            required=required,
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


def opt_taxon_id(required=True):
    def inner_func(func):
        return click.option(
            '-t',
            '--taxon-id',
            help='Taxon ID',
            type=click.STRING,
            required=required,
        )(func)
    return inner_func


def opt_fieldtype(required=True):
    def inner_func(func):
        return click.option(
            '-ft',
            '--field-type',
            required=required,
            help='Metadata field type. Use `austrakka fieldtype list` to see options.',
            type=click.STRING)(func)
    return inner_func


def opt_owner_group_roles(required=True):
    def inner_func(func):
        return click.option(
            '-ogr',
            '--owner-group-roles',
            type=click.Choice(get_role_list()),
            help='The user''s Owner group and role assignment. Exclude ' +
                 'this option if the user is not an owner.',
            required=required,
            multiple=True
        )(func)
    return inner_func


def opt_user_email(required=True):
    def inner_func(func):
        return click.option(
            '-e',
            '--email',
            type=str,
            help='User email',
            required=required
        )(func)
    return inner_func


def opt_is_active(is_update=False):
    def inner_func(func):
        return click.option(
            '--is-active/--not-active',
            default=None if is_update else True,
            type=bool,
            help='Determines if the entry is active'
        )(func)
    return inner_func


def opt_country(help_text='Country', required=True):
    def inner_func(func):
        return click.option(
            "--country",
            required=required,
            help=help_text,
            type=str
        )(func)
    return inner_func


def opt_state(help_text='State', required=True):
    def inner_func(func):
        return click.option(
            "--state",
            required=required,
            help=help_text,
            type=str,
            default=None,
        )(func)
    return inner_func
