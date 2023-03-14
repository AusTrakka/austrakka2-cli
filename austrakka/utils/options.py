import typing as t
import functools

import click

from austrakka.utils.enums.seq import SEQ_TYPES
from austrakka.utils.enums.seq import READS
from austrakka.utils.enums.seq import READ_BOTH
from austrakka.utils.misc import AusTrakkaCliOption


def _default_option_params(**default):
    def decorator(func):
        @functools.wraps(func)
        def inner_func(*args, **kwargs):
            default.update(kwargs)
            return func(*args, **default)
        return inner_func
    return decorator


@_default_option_params(
    required=True,
    help='Abbreviated name, for use with the CLI and in metadata uploads'
)
def opt_abbrev(**attrs: t.Any):
    return _create_option(
        "-a",
        "--abbrev",
        **attrs
    )


@_default_option_params(
    required=True,
    help='Name'
)
def opt_name(var_name='name', **attrs: t.Any):
    return _create_option(
        "-n",
        "--name",
        var_name,
        type=click.STRING,
        **attrs
    )


@_default_option_params(
    required=True,
    help='Group Name'
)
def opt_group_name(var_name='group_name', **attrs: t.Any):
    return _create_option(
        "-g",
        "--group-name",
        var_name,
        type=click.STRING,
        **attrs
    )


@_default_option_params(
    required=True,
    help='Name'
)
def opt_sample_id(**attrs: t.Any):
    return _create_option(
        "-s",
        "--sample-id",
        type=click.STRING,
        multiple=True,
        **attrs
    )


@_default_option_params(
    required=True,
    multiple=True,
    help='Field name to show for this project',
)
def opt_field_name(**attrs: t.Any):
    return _create_option(
        "-fn",
        "--field-names",
        type=click.STRING,
        **attrs
    )


@_default_option_params(
    required=True,
    default="",
    help='Human-readable description text'
)
def opt_description(**attrs: t.Any):
    return _create_option(
        '-d',
        '--description',
        type=click.STRING,
        **attrs
    )


@_default_option_params(
    required=True,
    multiple=False,
    help='Project Abbreviation'
)
def opt_project(**attrs: t.Any):
    return _create_option(
        '--project',
        type=click.STRING,
        **attrs
    )


@_default_option_params(
    required=True,
    multiple=False,
    help='Analysis definition name'
)
def opt_definition(var_name='definition', **attrs: t.Any):
    return _create_option(
        '--definition',
        var_name,
        type=click.STRING,
        **attrs
    )


@_default_option_params(
    required=True,
    help='Organisation abbreviation. Must match an organisation ' +
         'known to AusTrakka, use `austrakka org list` to see valid values',
)
def opt_organisation(**attrs: t.Any):
    return _create_option(
        '-o',
        '--org',
        type=click.STRING,
        **attrs
    )


@_default_option_params(
    required=True,
    multiple=True,
    help='Name of group.'
)
def opt_group(**attrs: t.Any):
    return _create_option(
        '-g',
        '--group-name',
        type=click.STRING,
        **attrs
    )


def opt_groups(**attrs: t.Any):
    return _create_option(
        '-g',
        '--group-names',
        multiple=True,
        type=click.STRING,
        **attrs
    )


@_default_option_params(
    required=True,
    help='Proforma abbreviation. Use `austrakka proforma list` '
         + 'to see options.',
)
def opt_proforma(**attrs: t.Any):
    return _create_option(
        '-p',
        '--proforma',
        type=click.STRING,
        **attrs
    )


@_default_option_params(
    required=False,
    help='CSV file'
)
def opt_csv(**attrs: t.Any):
    return _create_option(
        "--csv",
        "csv_file",
        type=click.File('rb'),
        default=None,
        **attrs
    )


@_default_option_params(
    required=True,
    help='Sequence format'
)
def opt_seq_type(**attrs: t.Any):
    return _create_option(
        "-t",
        '--type',
        'seq_type',
        type=click.Choice(SEQ_TYPES),
        **attrs
    )


@_default_option_params(
    required=True,
    help='The output directory where files are saved. The directory and any '
         ' sub-directories will be created beneath this as needed.',
)
def opt_output_dir(**attrs: t.Any):
    return _create_option(
        "-o",
        '--outdir',
        'output_dir',
        type=click.Path(exists=False),
        **attrs
    )


@_default_option_params(
    help=f'Fastq read. Defaults to {READ_BOTH}, meaning both 1 and 2',
    default=READ_BOTH,
)
def opt_read(**attrs: t.Any):
    return _create_option(
        "-r",
        '--read',
        'read',
        type=click.Choice(READS),
        **attrs
    )


@_default_option_params(
    required=True,
    help='Analysis Abbreviation'
)
def opt_analysis(**attrs: t.Any):
    return _create_option(
        '-a',
        '--analysis',
        type=click.STRING,
        **attrs
    )


@_default_option_params(
    required=True,
    help='Metadata field type. Use `austrakka fieldtype list` to see options.'
)
def opt_fieldtype(**attrs: t.Any):
    return _create_option(
        '-ft',
        '--field-type',
        type=click.STRING,
        **attrs
    )


@_default_option_params(
    required=True,
    multiple=True,
    help='The user''s Owner group and role assignment. Exclude ' +
         'this option if the user is not an owner.',
)
def opt_owner_group_roles(**attrs: t.Any):
    return _create_option(
        '-ogr',
        '--owner-group-roles',
        type=click.STRING,
        **attrs
    )


@_default_option_params(
    required=True,
    help='User object ID'
)
def opt_user_object_id(**attrs: t.Any):
    return _create_option(
        '-ui',
        '--user-id',
        type=click.STRING,
        **attrs
    )


@_default_option_params(
    help='Determines if the entry is active'
)
def opt_is_active(is_update=False, **attrs: t.Any):
    return _create_option(
        '--is-active/--not-active',
        type=bool,
        default=None if is_update else True,
        **attrs
    )


@_default_option_params(
    help='Specify validation mode (as if appending or creating) when checking data.'
)
def opt_is_append(**attrs: t.Any):
    return _create_option(
        '--is-append/--not-append',
        type=bool,
        default=False,
        **attrs
    )


@_default_option_params(
    required=True,
    help='Country'
)
def opt_country(**attrs: t.Any):
    return _create_option(
        "--country",
        type=click.STRING,
        **attrs
    )


@_default_option_params(
    required=True,
    help='State',
    default=None
)
def opt_state(**attrs: t.Any):
    return _create_option(
        "--state",
        type=click.STRING,
        **attrs
    )


@_default_option_params(
    required=True,
    help='Filter String'
)
def opt_filter_string(**attrs: t.Any):
    return _create_option(
        "--filter-str",
        type=click.STRING,
        **attrs
    )


@_default_option_params(
    required=True,
    multiple=True,
    help='Allowed value for this categorical field.',
)
def opt_fieldtype_value(var_name='values', **attrs: t.Any):
    return _create_option(
        '-v',
        '--value',
        var_name,
        type=click.STRING,
        **attrs
    )


@_default_option_params(
    required=False,
    multiple=True,
    help='The group and role to remove from the specified user. Use comma (,) '
         'as a separator. Format is <group>,<role> Eg. group1,role1',
)
def opt_group_role(**attrs: t.Any):
    return _create_option(
        '-gr',
        '--group-role',
        type=click.STRING,
        **attrs
    )


def _create_option(*param_decls: str, **attrs: t.Any):
    def inner_func(func):
        return click.option(
            *param_decls,
            cls=AusTrakkaCliOption,
            **attrs)(func)
    return inner_func
