# pylint: disable=consider-iterating-dictionary
import typing as t

import click

from austrakka.utils.enums.privilege_level import (
    AUSTRAKKA_ADMIN_LEVEL,
    FUNCTIONAL_ADMIN_LEVEL,
    USER_LEVEL)

from austrakka.utils.enums.seq import SeqType
from austrakka.utils.enums.view_type import MORE, COMPACT, FULL
from austrakka.utils.option_utils import create_option, MutuallyExclusiveOption


def opt_abbrev(**attrs: t.Any):
    defaults = {
        'required': True,
        'help': 'Abbreviated name, for use with the CLI and in metadata uploads'}
    return create_option(
        "-a",
        "--abbrev",
        **{**defaults, **attrs}
    )


def opt_tracking_token(**attrs: t.Any):
    defaults = {
        'required': True,
        'help': 'Tracking token for a dataset upload that can be used to query the upload status'
    }
    return create_option(
        "-tt",
        "--tracking_token",
        **{**defaults, **attrs}
    )


def opt_detailed(**attrs: t.Any):
    defaults = {
        'help': "Do you want to fetch more detailed tracking information"
    }
    return create_option(
        '--detailed',
        type=bool,
        is_flag=True,
        default=False,
        **{**defaults, **attrs}
    )


def opt_name(var_name='name', **attrs: t.Any):
    defaults = {
        'required': True,
        'help': 'Name',
    }
    return create_option(
        "-n",
        "--name",
        var_name,
        type=click.STRING,
        **{**defaults, **attrs}
    )


def opt_private(is_update=False, **attrs: t.Any):
    defaults = {
        'help': 'Determines if the field is private'
    }
    return create_option(
        '--is-private/--not-private',
        type=bool,
        default=None if is_update else False,
        **{**defaults, **attrs}
    )


def opt_email_address(var_name='email', **attrs: t.Any):
    defaults = {
        'required': True,
        'help': 'Email Address',
    }
    return create_option(
        "-e",
        "--email",
        var_name,
        type=click.STRING,
        **{**defaults, **attrs}
    )


def opt_dashboard_name(var_name='dashboard_name', **attrs: t.Any):
    defaults = {
        'required': True,
        'help': 'Dashboard name to assign to project',
    }
    return create_option(
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
    return create_option(
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
        'multiple': True,
    }
    return create_option(
        "-s",
        "--sample-id",
        type=click.STRING,
        **{**defaults, **attrs}
    )


def opt_prov_id(**attrs: t.Any):
    defaults = {
        'required': True,
        'help': 'provision id',
    }
    return create_option(
        "-pi",
        "--prov-id",
        type=click.STRING,
        **{**defaults, **attrs}
    )


def opt_field_name(**attrs: t.Any):
    defaults = {
        'required': True,
        'multiple': True,
        'help': 'Field name to show for this project',
    }
    return create_option(
        "-fn",
        "--field-names",
        type=click.STRING,
        **{**defaults, **attrs}
    )


def opt_new_name(**attrs: t.Any):
    defaults = {
        'required': True,
        'multiple': False,
        'help': 'New name to assign to an entity.',
    }
    return create_option(
        "-nn",
        "--new-name",
        type=click.STRING,
        **{**defaults, **attrs}
    )


def opt_description(**attrs: t.Any):
    defaults = {
        'required': True,
        'help': 'Human-readable description text',
    }
    return create_option(
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
    return create_option(
        '--project',
        type=click.STRING,
        **{**defaults, **attrs}
    )


def opt_definition(var_name='definition', **attrs: t.Any):
    defaults = {
        'multiple': False,
        'default': 'upload',
        'help': 'Analysis definition name',
    }
    return create_option(
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
    return create_option(
        '-o',
        '--org',
        type=click.STRING,
        **{**defaults, **attrs}
    )


def opt_email(**attrs: t.Any):
    defaults = {
        'required': False,
        'help': 'Email',
    }
    return create_option(
        '--email',
        type=click.STRING,
        **{**defaults, **attrs}
    )


def opt_proforma(**attrs: t.Any):
    defaults = {
        'required': True,
        'help': 'Proforma abbreviation. Use `austrakka proforma list` to see '
                'options.',
    }
    return create_option(
        '-p',
        '--proforma',
        type=click.STRING,
        **{**defaults, **attrs}
    )


def opt_analysis_label(**attrs: t.Any):
    defaults = {
        'required': True,
        'help': 'Analysis label to distinguish the same field across different '
                'datasets.',
    }
    return create_option(
        '-al',
        '--analysis-label',
        type=click.STRING,
        **{**defaults, **attrs}
    )


def opt_csv(**attrs: t.Any):
    defaults = {
        'required': False,
        'help': 'CSV file',
    }
    return create_option(
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
    return create_option(
        "-t",
        '--type',
        'seq_type',
        type=click.Choice([t.value for t in SeqType]),
        **{**defaults, **attrs}
    )


def opt_output_dir(**attrs: t.Any):
    defaults = {
        'required': True,
        'help': 'The output directory where files are saved. The directory and '
                'any sub-directories will be created beneath this as needed.',
    }
    return create_option(
        "-o",
        '--outdir',
        'output_dir',
        type=click.Path(exists=False),
        **{**defaults, **attrs}
    )


def opt_analysis(**attrs: t.Any):
    defaults = {
        'required': True,
        'help': 'Analysis Abbreviation',
    }
    return create_option(
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
    return create_option(
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
    return create_option(
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
    return create_option(
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
    return create_option(
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
    return create_option(
        '-ui',
        '--user-id',
        type=click.STRING,
        **{**defaults, **attrs}
    )


def opt_global_ids(**attrs: t.Any):
    defaults = {
        'required': True,
        'multiple': True,
        'help': 'The IDs of the entities. Use a comma (,) to separate '
                'multiple IDs.',
    }
    return create_option(
        '-gis',
        '--global-ids',
        type=click.STRING,
        **{**defaults, **attrs}
    )


def opt_batch_size(**attrs: t.Any):
    defaults = {
        'required': False,
        'help': 'Batch size for upload/download'
    }
    return create_option(
        '-bs',
        '--batch-size',
        type=click.INT,
        **{**defaults, **attrs}
    )


def opt_is_active(is_update=False, **attrs: t.Any):
    defaults = {
        'help': 'Determines if the entry is active'
    }
    return create_option(
        '--is-active/--not-active',
        type=bool,
        default=None if is_update else True,
        **{**defaults, **attrs}
    )


def opt_is_austrakka_process(**attrs: t.Any):
    defaults = {
        'help': 'Determines if the user is an AusTrakka process'
    }
    return create_option(
        '--is-austrakka-process/--not-austrakka-process',
        type=bool,
        required=True,
        **{**defaults, **attrs}
    )


def opt_skip_mutex_force(**attrs: t.Any):
    defaults = {
        'help': 'When able, skip action rather than fail. Cannot be used together with force.'
    }
    return create_option(
        '--skip',
        type=bool,
        is_flag=True,
        mutually_exclusive=["force"],
        cls=MutuallyExclusiveOption,
        **{**defaults, **attrs}
    )


def opt_force_mutex_skip(**attrs: t.Any):
    defaults = {
        'help': 'Forcefully perform action. Cannot be used together with skip.'
    }
    return create_option(
        '--force',
        type=bool,
        is_flag=True,
        mutually_exclusive=["skip"],
        cls=MutuallyExclusiveOption,
        **{**defaults, **attrs}
    )


def opt_is_update(**attrs: t.Any):
    defaults = {
        'help': 'Specify validation mode (as if updating or creating) when '
                'checking data.'
    }
    return create_option(
        '--is-update/--not-update',
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
    return create_option(
        '--recalculate-hashes',
        type=bool,
        is_flag=True,
        **{**defaults, **attrs}
    )


def opt_delete_all(**attrs: t.Any):
    defaults = {
        'help': 'Delete active and inactive entities. '
                'By default, only inactive entities are deleted.'
    }
    return create_option(
        '--delete-all',
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
    return create_option(
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
    return create_option(
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
    return create_option(
        "--state",
        type=click.STRING,
        **{**defaults, **attrs}
    )


def opt_filter_string(**attrs: t.Any):
    defaults = {
        'required': True,
        'help': 'Filter String',
    }
    return create_option(
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
    return create_option(
        '-v',
        '--value',
        var_name,
        type=click.STRING,
        **{**defaults, **attrs}
    )


def opt_record_global_id(**attrs: t.Any):
    defaults = {
        'required': True,
        'help': 'The record referenced by a privilege entry. Eg., ProjectId, etc..',
    }
    return create_option(
        '-rguid',
        '--record-global-id',
        type=click.STRING,
        **{**defaults, **attrs}
    )


def opt_scope_access_def_global_id(**attrs: t.Any):
    defaults = {
        'required': True,
        'help': 'The global id of the Scope Access Definition',
    }
    return create_option(
        '--scope-access-def-global-id',
        type=click.STRING,
        **{**defaults, **attrs}
    )


def opt_record_type(**attrs: t.Any):
    defaults = {
        'required': True,
        'help': 'Record type that is the subject of access control. ',
    }
    return create_option(
        '-rt',
        '--record-type',
        type=click.Choice(['Tenant', 'Organisation']),
        **{**defaults, **attrs}
    )


def opt_view_type(**attrs: t.Any):
    defaults = {
        'required': True,
        'help': 'The amount of data to return. ',
        'default': COMPACT,
    }
    return create_option(
        '-vt',
        '--view-type',
        type=click.Choice([COMPACT, MORE, FULL]),
        **{**defaults, **attrs}
    )


def opt_privilege_level(**attrs: t.Any):
    defaults = {
        'required': True,
        'help': 'A privilege level in the permission system. ',
    }
    return create_option(
        '-pv',
        '--privilege-level',
        type=click.Choice([AUSTRAKKA_ADMIN_LEVEL, FUNCTIONAL_ADMIN_LEVEL, USER_LEVEL]),
        **{**defaults, **attrs}
    )


def opt_allowed_record_types(**attrs: t.Any):
    defaults = {
        'required': True,
        'help': 'Name of each allowed record types where a role can be used to control access. ',
        'multiple': True,
    }
    return create_option(
        "-art",
        "--allowed-record-types",
        type=click.Choice(['Tenant', 'Organisation']),
        **{**defaults, **attrs}
    )


def opt_role(**attrs: t.Any):
    defaults = {
        'required': True,
        'help': 'The role name that is unique to the tenant.',
    }
    return create_option(
        "-r",
        "--role",
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
    return create_option(
        '-gr',
        '--group-role',
        type=click.STRING,
        **{**defaults, **attrs}
    )


def opt_field_and_source(**attrs: t.Any):
    defaults = {
        'required': True,
        'multiple': True,
        'help': 'The field and source to target for a specified dataset. Use '
                'comma (,) as a separator. Format is <field>,<source>,<hidden>. '
                'Where hidden is optional. '
                'Eg. field1,source1. or field2,source2,hidden '
                'Sources include: both, sample, dataset'
                'Hidden boolean is an optional flag to hide the field in the UI from the beginning',
    }
    return create_option(
        '-fs',
        '--field-source',
        type=click.STRING,
        **{**defaults, **attrs}
    )


def opt_show_disabled(**attrs: t.Any):
    defaults = {
        'help': 'Shows or hides disabled entities [default: --hide-disabled]'
    }
    return create_option(
        '--show-disabled/--hide-disabled',
        type=bool,
        default=False,
        **{**defaults, **attrs}
    )


def opt_merge_algorithm(**attrs: t.Any):
    defaults = {
        'required': True,
        'help': 'Determines which merge algorithm to use when merging datasets. '
        'Valid options are: show-all, override'}
    return create_option(
        '--merge-algorithm', '-ma',
        type=click.Choice(['show-all', 'override']),
        **{**defaults, **attrs}
    )


def opt_tree_id(**attrs: t.Any):
    defaults = {
        'required': True,
        'help': 'Tree ID',
    }
    return create_option(
        '--tree-id',
        type=click.INT,
        **{**defaults, **attrs}
    )


def opt_view_id(**attrs: t.Any):
    defaults = {
        'required': False,
        'help': 'Project metadata view ID',
    }
    return create_option(
        '--view-id',
        **{**defaults, **attrs}
    )


def opt_server_username(**attrs: t.Any):
    defaults = {
        'required': False,
        'help': 'Analysis Server Username',
    }
    return create_option(
        "--server-username",
        type=click.STRING,
        **{**defaults, **attrs}
    )
