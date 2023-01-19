import typing as t
import functools

import click
from click_option_group import optgroup

from austrakka.utils.enums.seq import SEQ_TYPES
from austrakka.utils.enums.seq import READS
from austrakka.utils.enums.seq import READ_BOTH
from austrakka.utils.misc import AusTrakkaCliOption
from austrakka.utils.misc import AusTrakkaCliGroupOption


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
def opt_abbrev(in_group=False, **attrs: t.Any):
    return _create_option(
        "-a",
        "--abbrev",
        in_group=in_group,
        **attrs
    )


@_default_option_params(
    required=True,
    help='Name'
)
def opt_name(in_group=False, var_name='name', **attrs: t.Any):
    return _create_option(
        "-n",
        "--name",
        var_name,
        type=click.STRING,
        in_group=in_group,
        **attrs
    )


@_default_option_params(
    required=True,
    help='Name'
)
def opt_sample_id(in_group=False, **attrs: t.Any):
    return _create_option(
        "-s",
        "--sample-id",
        type=click.STRING,
        multiple=True,
        in_group=in_group,
        **attrs
    )


@_default_option_params(
    required=True,
    multiple=True,
    help='Field name to show for this project',
)
def opt_field_name(in_group=False, **attrs: t.Any):
    return _create_option(
        "-fn",
        "--field-names",
        type=click.STRING,
        in_group=in_group,
        **attrs
    )


@_default_option_params(
    required=True,
    default="",
    help='Human-readable description text'
)
def opt_description(in_group=False, **attrs: t.Any):
    return _create_option(
        '-d',
        '--description',
        type=click.STRING,
        in_group=in_group,
        **attrs
    )


@_default_option_params(
    required=True,
    multiple=False,
    help='Species Abbreviation'
)
def opt_species(in_group=False, **attrs: t.Any):
    return _create_option(
        '-s',
        '--species',
        type=click.STRING,
        in_group=in_group,
        **attrs
    )


@_default_option_params(
    required=True,
    multiple=False,
    help='Project Abbreviation'
)
def opt_project(in_group=False, **attrs: t.Any):
    return _create_option(
        '--project',
        type=click.STRING,
        in_group=in_group,
        **attrs
    )


@_default_option_params(
    required=True,
    multiple=False,
    help='Analysis definition name'
)
def opt_definition(in_group=False, var_name='definition', **attrs: t.Any):
    return _create_option(
        '--definition',
        var_name,
        type=click.STRING,
        in_group=in_group,
        **attrs
    )


@_default_option_params(
    required=True,
    help='Organisation abbreviation. Must match an organisation ' +
         'known to AusTrakka, use `austrakka org list` to see valid values',
)
def opt_organisation(in_group=False, **attrs: t.Any):
    return _create_option(
        '-o',
        '--org',
        type=click.STRING,
        in_group=in_group,
        **attrs
    )


@_default_option_params(
    required=True,
    multiple=True,
    help='Name of group.'
)
def opt_group(in_group=False, **attrs: t.Any):
    return _create_option(
        '-g',
        '--group-name',
        type=click.STRING,
        in_group=in_group,
        **attrs
    )


def opt_groups(in_group=False, **attrs: t.Any):
    return _create_option(
        '-g',
        '--group-names',
        multiple=True,
        type=click.STRING,
        in_group=in_group,
        **attrs
    )


@_default_option_params(
    required=True,
    help='Proforma abbreviation. Use `austrakka proforma list` '
         + 'to see options.',
)
def opt_proforma(in_group=False, **attrs: t.Any):
    return _create_option(
        '-p',
        '--proforma',
        type=click.STRING,
        in_group=in_group,
        **attrs
    )


@_default_option_params(
    required=False,
    help='CSV file'
)
def opt_csv(in_group=False, **attrs: t.Any):
    return _create_option(
        "--csv",
        "csv_file",
        type=click.File('rb'),
        default=None,
        in_group=in_group,
        **attrs
    )


@_default_option_params(
    required=True,
    help='Sequence format'
)
def opt_seq_type(in_group=False, **attrs: t.Any):
    return _create_option(
        "-t",
        '--type',
        'seq_type',
        type=click.Choice(SEQ_TYPES),
        in_group=in_group,
        **attrs
    )


@_default_option_params(
    required=True,
    help='The output directory where files are saved. The directory and any '
         ' sub-directories will be created beneath this as needed.',
)
def opt_output_dir(in_group=False, **attrs: t.Any):
    return _create_option(
        "-o",
        '--outdir',
        'output_dir',
        type=click.Path(exists=False),
        in_group=in_group,
        **attrs
    )


@_default_option_params(
    help=f'Fastq read. Defaults to {READ_BOTH}, meaning both 1 and 2',
    default=READ_BOTH,
)
def opt_read(in_group=False, **attrs: t.Any):
    return _create_option(
        "-r",
        '--read',
        'read',
        type=click.Choice(READS),
        in_group=in_group,
        **attrs
    )


@_default_option_params(
    required=True,
    help='Analysis Abbreviation'
)
def opt_analysis(in_group=False, **attrs: t.Any):
    return _create_option(
        '-a',
        '--analysis',
        type=click.STRING,
        in_group=in_group,
        **attrs
    )


@_default_option_params(
    required=True,
    help='Metadata field type. Use `austrakka fieldtype list` to see options.'
)
def opt_fieldtype(in_group=False, **attrs: t.Any):
    return _create_option(
        '-ft',
        '--field-type',
        type=click.STRING,
        in_group=in_group,
        **attrs
    )


@_default_option_params(
    required=True,
    multiple=True,
    help='The user''s Owner group and role assignment. Exclude ' +
         'this option if the user is not an owner.',
)
def opt_owner_group_roles(in_group=False, **attrs: t.Any):
    return _create_option(
        '-ogr',
        '--owner-group-roles',
        type=click.STRING,
        in_group=in_group,
        **attrs
    )


@_default_option_params(
    required=True,
    help='User object ID'
)
def opt_user_object_id(in_group=False, **attrs: t.Any):
    return _create_option(
        '-ui',
        '--user-id',
        type=click.STRING,
        in_group=in_group,
        **attrs
    )


@_default_option_params(
    help='Determines if the entry is active'
)
def opt_is_active(in_group=False, is_update=False, **attrs: t.Any):
    return _create_option(
        '--is-active/--not-active',
        type=bool,
        in_group=in_group,
        default=None if is_update else True,
        **attrs
    )


@_default_option_params(
    help='Specify validation mode (as if appending or creating) when checking data.'
)
def opt_is_append(in_group=False, **attrs: t.Any):
    return _create_option(
        '--is-append/--not-append',
        type=bool,
        in_group=in_group,
        default=False,
        **attrs
    )


@_default_option_params(
    required=True,
    help='Country'
)
def opt_country(in_group=False, **attrs: t.Any):
    return _create_option(
        "--country",
        type=click.STRING,
        in_group=in_group,
        **attrs
    )


@_default_option_params(
    required=True,
    help='State',
    default=None
)
def opt_state(in_group=False, **attrs: t.Any):
    return _create_option(
        "--state",
        type=click.STRING,
        in_group=in_group,
        **attrs
    )


@_default_option_params(
    required=True,
    help='Filter String'
)
def opt_filter_string(in_group=False, **attrs: t.Any):
    return _create_option(
        "--filter-str",
        type=click.STRING,
        in_group=in_group,
        **attrs
    )


@_default_option_params(
    required=True,
    multiple=True,
    help='Allowed value for this categorical field.',
)
def opt_fieldtype_value(in_group=False, var_name='values', **attrs: t.Any):
    return _create_option(
        '-v',
        '--value',
        var_name,
        type=click.STRING,
        in_group=in_group,
        **attrs
    )


@_default_option_params(
    required=False,
    multiple=True,
    help='The group and role to remove from the specified user. Use comma (,) '
         'as a separator. Format is <group>,<role> Eg. group1,role1',
)
def opt_group_role(in_group=False, **attrs: t.Any):
    return _create_option(
        '-gr',
        '--group-role',
        type=click.STRING,
        in_group=in_group,
        **attrs
    )


def _create_option(*param_decls: str, in_group: bool, **attrs: t.Any):
    def inner_func(func):
        if in_group:
            # This will cause issues for a non-mutually exclusive group.
            # We can deal with it when/if it comes up.
            attrs.pop('required')
            attrs['cls'] = AusTrakkaCliGroupOption
            return optgroup.option(*param_decls, **attrs)(func)
        attrs['cls'] = AusTrakkaCliOption
        return click.option(*param_decls, **attrs)(func)
    return inner_func
