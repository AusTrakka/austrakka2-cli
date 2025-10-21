import typing as t
from io import BufferedReader

import click

from austrakka.utils.misc import logger_wraps


def create_option(*param_decls: str, **attrs: t.Any):
    def inner_func(func):
        if 'cls' in attrs:
            return click.option(
                *param_decls,
                show_default=True,
                **attrs)(func)

        return click.option(
            *param_decls,
            cls=AusTrakkaCliOption,
            show_default=True,
            **attrs)(func)

    return inner_func


def _get_custom_help_record(orig_help, multiple):
    if multiple:
        tmp_list = list(orig_help)
        split_str = tmp_list[len(tmp_list) - 1].rsplit("]", 1)
        if len(split_str) > 1:
            tmp_list[len(tmp_list) - 1] = split_str[0] + ";Accepts Multiple]"
        else:
            tmp_list[len(tmp_list) - 1] += " [Accepts Multiple]"
        orig_help = tuple(tmp_list)
    return orig_help


class AusTrakkaCliOption(click.Option):
    def get_help_record(self, ctx):
        orig_help = super().get_help_record(ctx)
        return _get_custom_help_record(orig_help, self.multiple)


class MutuallyExclusiveOption(AusTrakkaCliOption):
    def __init__(self, *args, **kwargs):
        self.mutually_exclusive = set(kwargs.pop('mutually_exclusive', []))
        help_text = kwargs.get('help', '')
        if self.mutually_exclusive:
            ex_str = ', '.join([fld.replace('_','-') for fld in self.mutually_exclusive])
            kwargs['help'] = help_text + (
                    ' Mutually exclusive with [' + ex_str + '].'
            )
        super().__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):
        if self.mutually_exclusive.intersection(opts) and self.name in opts:
            raise click.UsageError(
                f"`{self.name.replace('_','-')}` is mutually exclusive "
                f"with `{', '.join([fld.replace('_','-') for fld in self.mutually_exclusive])}`."
            )

        return super().handle_parse_result(
            ctx,
            opts,
            args
        )


class RequiredMutuallyExclusiveOption(AusTrakkaCliOption):
    def __init__(self, *args, **kwargs):
        self.mutually_exclusive = set(kwargs.pop('mutually_exclusive', []))
        help_text = kwargs.get('help', '')
        if self.mutually_exclusive:
            ex_str = ', '.join([fld.replace('_','-') for fld in self.mutually_exclusive])
            kwargs['help'] = help_text + (
                    ' [Mutually exclusive with ' + ex_str + ';'
                    'At least one of these options are required]'
            )
        super().__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):
        mutex_display_names = [fld.replace('_','-') for fld in self.mutually_exclusive]
        if self.mutually_exclusive.intersection(opts) and self.name in opts:
            raise click.UsageError(
                f" `{self.name.replace('_','-')}` is mutually exclusive "
                f"with `{', '.join(mutex_display_names)}`."
            )
        if not self.mutually_exclusive.intersection(opts) and self.name not in opts:
            raise click.UsageError(
                f" You must provide at least one of these arguments: "
                f"`{', '.join([self.name.replace('_','-')] + list(mutex_display_names))}`."
            )

        return super().handle_parse_result(
            ctx,
            opts,
            args
        )

@logger_wraps()
def get_seq_list(
        seq_ids: [str] = None,
        file: BufferedReader = None,
):
    if file is None and (seq_ids is None or len(seq_ids) == 0):
        raise ValueError(
            "Either Seq_IDs or file must be provided to share sequences")

    if file:
        seq_id_list = [line.decode("utf-8").strip() for line in file if line.strip()]
    else:
        seq_id_list = list(seq_ids)

    return seq_id_list
