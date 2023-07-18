import click
from click import option

from austrakka.utils.options import opt_output_dir
from austrakka.utils.options import opt_group
from austrakka.utils.options import opt_recalc_hash
from austrakka.utils.options import opt_seq_type
from austrakka.utils.options import opt_download_batch_size
from .funcs import seq_get


@click.group()
@click.pass_context
def sync(ctx):
    """Commands to sync sequences from server to disk"""
    ctx.context = ctx.parent.context


@sync.command('get')
@opt_output_dir()
@opt_group(default=None, multiple=False, required=True)
@opt_recalc_hash()
@opt_seq_type(required=True)
@opt_download_batch_size()
@option('--reset', help="Reset sync state; do not try to resume an "
                        "interrupted sync", is_flag=True)
def get_seq(
        output_dir: str,
        group_name: str,
        recalculate_hashes: bool,
        seq_type: str,
        batch_size: int,
        reset: bool):
    """
    Download sequence files from server to disk. Patches any local
    files that have drifted, and soft-purge local files which are
    no longer shared with the group.
    """
    seq_get(
        output_dir,
        group_name,
        recalculate_hashes,
        seq_type,
        batch_size,
        reset)
