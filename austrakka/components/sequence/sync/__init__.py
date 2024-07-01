import click
from click import option

from austrakka.utils.options import opt_output_dir, opt_group_name
from austrakka.utils.options import opt_recalc_hash
from austrakka.utils.options import opt_seq_type
from austrakka.utils.options import opt_batch_size
from .funcs import seq_sync_get, seq_sync_migrate


@click.group()
@click.pass_context
def sync(ctx):
    """Commands to sync sequences from server to disk"""
    ctx.context = ctx.parent.context

@sync.command('migrate')
@opt_output_dir()
def sync_migrate(output_dir: str):
    """
    Migrate sequence files from the old sync system to the new one.
    """
    seq_sync_migrate(output_dir)

@sync.command('get')
@opt_output_dir()
@opt_group_name(default=None, multiple=False, required=True)
@opt_recalc_hash()
@opt_seq_type(required=True)
@opt_batch_size(help='Specifies the number of sequence downloads to perform '
                     'in a single batch during sync. This may improve '
                     'performance depending on how many total sequences are expected. '
                     'When resuming from an interruption, the '
                     'entire batch will be re-tried even if some within a '
                     'batch might have succeeded. For large fastq files, the '
                     'recommended size is 1 to 10. For large numbers of small '
                     'fasta files, the recommended size is 1000 or more.',
                default=1)
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
    seq_sync_get(
        output_dir,
        group_name,
        recalculate_hashes,
        seq_type,
        batch_size,
        reset)
