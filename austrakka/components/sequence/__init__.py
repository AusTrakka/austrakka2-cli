# pylint: disable=redefined-outer-name
from io import BufferedReader

import click

from austrakka.utils.output import table_format_option
from austrakka.utils.options import opt_seq_type, opt_seq_filter
from austrakka.utils.options import opt_output_dir
from austrakka.utils.options import opt_read
from austrakka.utils.options import opt_group

from .funcs import take_sample_names
from .funcs import get_sequences
from .funcs import list_sequences
from .add import add
from .sync import sync


@click.group()
@click.pass_context
def seq(ctx):
    """Commands related to sequences"""
    ctx.context = ctx.parent.context


seq.add_command(add)
seq.add_command(sync)


@seq.command('get')
@opt_output_dir()
@opt_seq_type()
@opt_read()
@opt_group(default=None, multiple=False, required=True)
@opt_seq_filter(multiple=False, required=False)
def get(
        output_dir,
        seq_type: str,
        read: str,
        group_name: str,
        sub_query_type: str,
):
    """Download sequence files to the local drive

    EXAMPLE: Download Fasta for group Example-Group

        austrakka seq get -t fasta --group-name Example-Group --outdir ~/Downloads/fasta-files


    """
    get_sequences(
        output_dir,
        seq_type,
        read,
        group_name,
        sub_query_type,
    )


@seq.command('list')
@table_format_option()
@opt_seq_type(default=None, required=False)
@opt_read()
@opt_group(default=None, multiple=False, required=True)
@opt_seq_filter(multiple=False, required=False)
def seq_list(
        out_format: str,
        seq_type: str,
        read: str,
        group_name: str,
        sub_query_type: str,
):
    list_sequences(
        out_format,
        seq_type,
        read,
        group_name,
        sub_query_type,
    )
