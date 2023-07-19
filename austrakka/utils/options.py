import typing as t

import click
from click import Option, UsageError

from austrakka.utils.enums.seq import SEQ_TYPES, SEQ_FILTERS
from austrakka.utils.enums.seq import READS, BY_LATEST_DATE
from austrakka.utils.enums.seq import READ_BOTH
from austrakka.utils.misc import AusTrakkaCliOption


class MutuallyExclusiveOption(Option):
    def __init__(self, *args, **kwargs):
        self.mutually_exclusive = set(kwargs.pop('mutually_exclusive', []))
        help_text = kwargs.get('help', '')
        if self.mutually_exclusive:
            ex_str = ', '.join(self.mutually_exclusive)
            kwargs['help'] = help_text + (
                ' Mutually exclusive with [' + ex_str + '].'
            )
        super().__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):
        if self.mutually_exclusive.intersection(opts) and self.name in opts:
            raise UsageError(
                f"`{self.name}` is mutually exclusive "
                f"with `{', '.join(self.mutually_exclusive)}`."
            )

        return super().handle_parse_result(
            ctx,
            opts,
            args
        )


def opt_abbrev(**attrs: t.Any):
    defaults = {
        'required': True,
        'help': 'Abbreviated name, for use with the CLI and in metadata uploads'}
    return _create_option(
        "-a",
        "--abbrev",
        **{**defaults, **attrs}
    )


def opt_name(var_name='name', **attrs: t.Any):
    defaults = {
        'required': True,
        'help': 'Name',
    }
    return _create_option(
        "-n",
        "--name",
        var_name,
        type=click.STRING,
        **{**defaults, **attrs}
    )


def opt_dashboard_name(var_name='dashboard_name', **attrs: t.Any):
    defaults = {
        'required': True,
        'help': 'Dashboard name to assign to project',
    }
    return _create_option(
        "-dn",
        "--dashboard-name",
        var_name,
        type=click.STRING,
        **{**defaults, **attrs}
    )


def opt_group_name(var_name='group_name', **attrs: t.Any):
    defaults = {
        'required': True,
        'help': 'Group Name',
    }
    return _create_option(
        "-g",
        "--group-name",
        var_name,
        type=click.STRING,
        **{**defaults, **attrs}
    )


def opt_sample_id(**attrs: t.Any):
    defaults = {
        'required': True,
        'help': 'name',
    }
    return _create_option(
        "-s",
        "--sample-id",
        type=click.STRING,
        multiple=True,
        **{**defaults, **attrs}
    )


def opt_field_name(**attrs: t.Any):
    defaults = {
        'required': True,
        'multiple': True,
        'help': 'Field name to show for this project',
    }
    return _create_option(
        "-fn",
        "--field-names",
        type=click.STRING,
        **{**defaults, **attrs}
    )


def opt_widget(**attrs: t.Any):
    defaults = {
        'required': False,
        'multiple': True,
        'help': 'Comma separated definition of a widgets to assign to a dashboard.'
                'The format is [name,order,width]. eg. widget1,3,4',
    }
    return _create_option(
        "-wd",
        "--widget-details",
        type=click.STRING,
        **{**defaults, **attrs}
    )


def opt_new_name(**attrs: t.Any):
    defaults = {
        'required': True,
        'multiple': False,
        'help': 'New name to assign to an entity.',
    }
    return _create_option(
        "-nn",
        "--new-name",
        type=click.STRING,
        **{**defaults, **attrs}
    )


def opt_description(**attrs: t.Any):
    defaults = {
        'required': True,
        'default': '',
        'help': 'Human-readable description text',
    }
    return _create_option(
        '-d',
        '--description',
        type=click.STRING,
        **{**defaults, **attrs}
    )


def opt_project(**attrs: t.Any):
    defaults = {
        'required': True,
        'multiple': False,
        'help': 'Project Abbreviation',
    }
    return _create_option(
        '--project',
        type=click.STRING,
        **{**defaults, **attrs}
    )


def opt_definition(var_name='definition', **attrs: t.Any):
    defaults = {
        'required': True,
        'multiple': False,
        'help': 'Analysis definition name',
    }
    return _create_option(
        '--definition',
        var_name,
        type=click.STRING,
        **{**defaults, **attrs}
    )


def opt_organisation(**attrs: t.Any):
    defaults = {
        'required': True,
        'help': 'Organisation abbreviation. Must match an organisation ' +
                'known to AusTrakka, use `austrakka org list` to see valid ' +
                'values',
    }
    return _create_option(
        '-o',
        '--org',
        type=click.STRING,
        **{**defaults, **attrs}
    )


def opt_group(**attrs: t.Any):
    defaults = {
        'required': True,
        'multiple': True,
        'help': 'Name of group.'
    }
    return _create_option(
        '-g',
        '--group-name',
        type=click.STRING,
        **{**defaults, **attrs}
    )


def opt_groups(**attrs: t.Any):
    return _create_option(
        '-g',
        '--group-names',
        multiple=True,
        type=click.STRING,
        **attrs
    )


def opt_proforma(**attrs: t.Any):
    defaults = {
        'required': True,
        'help': 'Proforma abbreviation. Use `austrakka proforma list` to see '
                'options.',
    }
    return _create_option(
        '-p',
        '--proforma',
        type=click.STRING,
        **{**defaults, **attrs}
    )


def opt_csv(**attrs: t.Any):
    defaults = {
        'required': False,
        'help': 'CSV file',
    }
    return _create_option(
        "--csv",
        "csv_file",
        type=click.File('rb'),
        default=None,
        **{**defaults, **attrs}
    )


def opt_seq_type(**attrs: t.Any):
    defaults = {
        'required': True,
        'help': 'Sequence format',
    }
    return _create_option(
        "-t",
        '--type',
        'seq_type',
        type=click.Choice(SEQ_TYPES),
        **{**defaults, **attrs}
    )


def opt_seq_filter(**attrs: t.Any):
    defaults = {
        'required': False,
        'default': BY_LATEST_DATE,
        'help': 'addition filter for sequence.',
    }
    return _create_option(
        "-q",
        '--sub-seq-query',
        'sub_query_type',
        type=click.Choice(SEQ_FILTERS),
        **{**defaults, **attrs}
    )


def opt_output_dir(**attrs: t.Any):
    defaults = {
        'required': True,
        'help': 'The output directory where files are saved. The directory and '
                'any sub-directories will be created beneath this as needed.',
    }
    return _create_option(
        "-o",
        '--outdir',
        'output_dir',
        type=click.Path(exists=False),
        **{**defaults, **attrs}
    )


def opt_read(**attrs: t.Any):
    defaults = {
        'help': f'Fastq read. Defaults to {READ_BOTH}, meaning both 1 and 2',
        'default': READ_BOTH,
    }
    return _create_option(
        "-r",
        '--read',
        'read',
        type=click.Choice(READS),
        **{**defaults, **attrs}
    )


def opt_analysis(**attrs: t.Any):
    defaults = {
        'required': True,
        'help': 'Analysis Abbreviation',
    }
    return _create_option(
        '-a',
        '--analysis',
        type=click.STRING,
        **{**defaults, **attrs}
    )


def opt_fieldtype(**attrs: t.Any):
    defaults = {
        'required': True,
        'help': 'Metadata field type. Use `austrakka fieldtype list` to see '
                'options.'
    }
    return _create_option(
        '-ft',
        '--field-type',
        type=click.STRING,
        **{**defaults, **attrs}
    )


def opt_plottype(**attrs: t.Any):
    defaults = {
        'required': True,
        'help': 'Plot type. Use `austrakka plot types` to see options.'
    }
    return _create_option(
        '-pt',
        '--plottype',
        type=click.STRING,
        **{**defaults, **attrs}
    )


def opt_plotspec(**attrs: t.Any):
    defaults = {
        'required': False,
        'help': 'Plot spec. If not provided, or empty, the default spec for the'
        ' plot type will be used.'}
    return _create_option(
        '-spec',
        'spec',
        type=click.File('r'),
        **{**defaults, **attrs}
    )


def opt_owner_group_roles(**attrs: t.Any):
    defaults = {
        'required': True,
        'multiple': True,
        'help': 'The user''s Owner group and role assignment. Exclude ' +
                'this option if the user is not an owner.',
    }
    return _create_option(
        '-ogr',
        '--owner-group-roles',
        type=click.STRING,
        **{**defaults, **attrs}
    )


def opt_user_object_id(**attrs: t.Any):
    defaults = {
        'required': True,
        'help': 'User object ID',
    }
    return _create_option(
        '-ui',
        '--user-id',
        type=click.STRING,
        **{**defaults, **attrs}
    )


def opt_download_batch_size(**attrs: t.Any):
    defaults = {
        'required': False,
        'help': 'Specifies the number of sequence downloads to perform '
                'in a single batch during sync. This could improve '
                'performance depending on how many total sequences are expected. '
                'When resuming from an interruption, the '
                'entire batch would be re-tried even if some within a '
                'batch might have succeeded. For large fastq files, the '
                'recommended size is 1 to 10. For large numbers of small '
                'fasta files, the recommended size is 1000. Default is 1.',
    }
    return _create_option(
        '-bs',
        '--batch-size',
        type=click.INT,
        default=1,
        **{**defaults, **attrs}
    )


def opt_is_active(is_update=False, **attrs: t.Any):
    defaults = {
        'help': 'Determines if the entry is active'
    }
    return _create_option(
        '--is-active/--not-active',
        type=bool,
        default=None if is_update else True,
        **{**defaults, **attrs}
    )


def opt_is_append(**attrs: t.Any):
    defaults = {
        'help': 'Specify validation mode (as if appending or creating) when '
                'checking data.'
    }
    return _create_option(
        '--is-append/--not-append',
        type=bool,
        default=False,
        **{**defaults, **attrs}
    )


def opt_recalc_hash(**attrs: t.Any):
    defaults = {
        'help': 'When comparing server file hashes to local file hashes, '
                'recalculate local file hashes for previously-downloaded '
                'files; do not use cached hashes. This can take a long '
                'time to run. This option may be useful if local files or '
                'cached hash values have been corrupted. If this option is '
                'not specified, cached local hashes will be used for '
                'previously-downloaded files, but hashes will still be '
                'calculated for newly-downloaded files.'
    }
    return _create_option(
        '--recalculate-hashes',
        type=bool,
        is_flag=True,
        **{**defaults, **attrs}
    )


def opt_blanks_delete(**attrs: t.Any):
    defaults = {
        'help': "Blank cells in the CSV / Excel file will "
                "be treated as a delete command for that cell. By "
                "default, blank cells are ignored."
    }
    return _create_option(
        '--blanks-will-delete',
        type=bool,
        is_flag=True,
        default=False,
        **{**defaults, **attrs}
    )


def opt_country(**attrs: t.Any):
    defaults = {
        'required': True,
        'help': 'Country',
    }
    return _create_option(
        "--country",
        type=click.STRING,
        **{**defaults, **attrs}
    )


def opt_state(**attrs: t.Any):
    defaults = {
        'required': True,
        'help': 'State',
        'default': None,
    }
    return _create_option(
        "--state",
        type=click.STRING,
        **{**defaults, **attrs}
    )


def opt_filter_string(**attrs: t.Any):
    defaults = {
        'required': True,
        'help': 'Filter String',
    }
    return _create_option(
        "--filter-str",
        type=click.STRING,
        **{**defaults, **attrs}
    )


def opt_fieldtype_value(var_name='values', **attrs: t.Any):
    defaults = {
        'required': True,
        'multiple': True,
        'help': 'Allowed value for this categorical field.',
    }
    return _create_option(
        '-v',
        '--value',
        var_name,
        type=click.STRING,
        **{**defaults, **attrs}
    )


def opt_group_role(**attrs: t.Any):
    defaults = {
        'required': False,
        'multiple': True,
        'help': 'The group and role to remove from the specified user. Use '
                'comma (,) as a separator. Format is <group>,<role> '
                'Eg. group1,role1',
    }
    return _create_option(
        '-gr',
        '--group-role',
        type=click.STRING,
        **{**defaults, **attrs}
    )


def opt_show_disabled(**attrs: t.Any):
    defaults = {
        'help': 'Shows or hides disabled entities [default: --hide-disabled]'
    }
    return _create_option(
        '--show-disabled/--hide-disabled',
        type=bool,
        default=False,
        **{**defaults, **attrs}
    )


def _create_option(*param_decls: str, **attrs: t.Any):
    def inner_func(func):
        return click.option(
            *param_decls,
            cls=AusTrakkaCliOption,
            **attrs)(func)
    return inner_func
