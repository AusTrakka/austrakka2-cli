import click

from austrakka.utils.options import opt_output_dir
from austrakka.utils.options import opt_group
from austrakka.utils.options import opt_hash_check
from austrakka.utils.options import opt_seq_type
from .funcs import seq_get


@click.group()
@click.pass_context
def sync(ctx):
    """Commands to sync sequences from server to disk"""
    ctx.context = ctx.parent.context


@sync.command('get')
@opt_output_dir()
@opt_group(default=None, multiple=False, required=True)
@opt_hash_check()
@opt_seq_type(required=True)
def get_seq(output_dir: str, group_name: str, hash_check: bool, seq_type: str):
    """
    Download sequence files from server to disk. Patches any local
    files that have drifted, and soft-purge local files which are
    no longer shared with the group.
    """
    seq_get(output_dir, group_name, hash_check, seq_type)
