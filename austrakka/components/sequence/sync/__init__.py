import click

from austrakka.utils.options import opt_output_dir
from austrakka.utils.options import opt_group
from austrakka.utils.options import opt_hash_check
from .funcs import fastq_sync


@click.group()
@click.pass_context
def sync(ctx):
    """Commands to sync sequences from server to disk"""
    ctx.context = ctx.parent.context


@sync.command('fastq')
@opt_output_dir()
@opt_group(default=None, multiple=False, required=True)
@opt_hash_check()
def get_fastq(output_dir: str, group_name: str, hash_check: bool):
    """
    Download fastq files from server to disk. Patches any local
    files that have drifted, and soft-purge local files which are
    no longer shared with the group.
    """
    fastq_sync(output_dir, group_name, hash_check)
