import os.path

from loguru import logger

from austrakka.utils.misc import logger_wraps
from austrakka.utils.fs import create_dir
from .sync_state import initialise, load_state, load_old_state
from .sync_workflow import select_start_state, configure_state_machine, reset, list_expected_headers
from .state_machine import SName
from .sync_io import save_json, read_from_csv, get_path, save_to_csv

from .constant import SEQ_ID_KEY
from .constant import SYNC_STATE_FILE
from .constant import MANIFEST_FILE_NAME
from .constant import INTERMEDIATE_MANIFEST_FILE
from .constant import OBSOLETE_OBJECTS_FILE
from .constant import FASTA_AGGREGATE_FILE_NAME
from .constant import OUTPUT_DIR_KEY
from .constant import CURRENT_STATE_KEY
from .constant import GROUP_NAME_KEY
from .constant import SEQ_TYPE_KEY
from .constant import RECALCULATE_HASH_KEY
from .constant import DOWNLOAD_BATCH_SIZE_KEY
from .constant import SYNC_STATE_FILE_KEY
from .constant import INTERMEDIATE_MANIFEST_FILE_KEY
from .constant import MANIFEST_KEY
from .constant import OBSOLETE_OBJECTS_FILE_KEY
from .constant import OLD_SYNC_STATE_FILE
from .constant import OLD_INTERMEDIATE_MANIFEST_FILE
from .constant import OLD_MANIFEST_FILE
from .constant import OLD_OBJS_FILE
from .constant import OLD_FASTA_AGGREGATE_FILE_NAME
from .constant import MIGRATE_SEQ_TYPES


@logger_wraps()
def seq_sync_get(
        output_dir: str,
        group_name: str,
        recalc_hash: bool,
        seq_type: str,
        download_batch_size: int,
        reset_opt: bool):

    sync_state = {}
    state_file_path = os.path.join(output_dir, SYNC_STATE_FILE.replace('SEQTYPE', seq_type))

    if os.path.exists(state_file_path):
        sync_state = load_state(
            group_name,
            output_dir,
            state_file_path,
            seq_type)

        # We just opened the file, so it has to be set to
        # the same file name for later use. It's probably
        # already the same thing. This will guarantee that.
        sync_state[SYNC_STATE_FILE_KEY] = SYNC_STATE_FILE.replace('SEQTYPE', seq_type)

        # Settings allowed to be overriden between runs.
        sync_state[RECALCULATE_HASH_KEY] = recalc_hash
        sync_state[DOWNLOAD_BATCH_SIZE_KEY] = download_batch_size
        save_json(sync_state, state_file_path)

    elif not os.path.exists(output_dir):
        create_dir(output_dir)

    if CURRENT_STATE_KEY not in sync_state:
        sync_state = initialise(
            group_name,
            recalc_hash,
            output_dir,
            seq_type,
            download_batch_size)

        save_json(sync_state, state_file_path)

    if reset_opt:
        reset(state_file_path, sync_state)
    else:
        select_start_state(state_file_path, sync_state)

    logger.info('Starting sync with args..')
    logger.info(f'{OUTPUT_DIR_KEY}: {sync_state[OUTPUT_DIR_KEY]}')
    logger.info(f'{GROUP_NAME_KEY}: {sync_state[GROUP_NAME_KEY]}')
    logger.info(f'{SEQ_TYPE_KEY}: {sync_state[SEQ_TYPE_KEY]}')
    logger.info(f'{RECALCULATE_HASH_KEY}: {sync_state[RECALCULATE_HASH_KEY]}')

    state_machine = configure_state_machine()
    state_machine.run(sync_state)
    logger.success("Sync completed")

@logger_wraps()
def seq_sync_migrate(output_dir: str):
    logger.info("Looking for old sync state file.")
    state_file_path = os.path.join(output_dir, OLD_SYNC_STATE_FILE)
    
    if not os.path.exists(state_file_path):
        logger.info("No old sync state file found.")
        return

    sync_state = load_old_state(
        output_dir,
        state_file_path)
    
    old_seq_type = sync_state[SEQ_TYPE_KEY]
    if old_seq_type not in MIGRATE_SEQ_TYPES:
        logger.info(f"Old seq type {old_seq_type} is not supported for migration.")
        return
    seq_type = MIGRATE_SEQ_TYPES[old_seq_type]
    logger.info(f"Found state for seq type {old_seq_type}, will migrate to {seq_type}.")

    # Read old manifest before updating state and paths
    if not os.path.exists(os.path.join(output_dir, OLD_MANIFEST_FILE)):
        logger.error("Old manifest file not found, cannot proceed with migration. "+
                     "Has the migration already occured?")
        return
    manifest = read_from_csv(sync_state, MANIFEST_KEY)

    # Update state
    sync_state[SEQ_TYPE_KEY] = seq_type
    sync_state[SYNC_STATE_FILE_KEY] = SYNC_STATE_FILE.replace('SEQTYPE', seq_type)
    sync_state[MANIFEST_KEY] = MANIFEST_FILE_NAME.replace('SEQTYPE', seq_type)
    sync_state[INTERMEDIATE_MANIFEST_FILE_KEY] = \
        INTERMEDIATE_MANIFEST_FILE.replace('SEQTYPE', seq_type)
    sync_state[OBSOLETE_OBJECTS_FILE_KEY] = OBSOLETE_OBJECTS_FILE.replace('SEQTYPE', seq_type)

    # Proceed only if in the correct state and intermediate files do not exist
    if sync_state[CURRENT_STATE_KEY] != SName.UP_TO_DATE:
        logger.error("Cannot proceed with migration, sync state is not up to date.")
        return
    if os.path.exists(os.path.join(output_dir, OLD_INTERMEDIATE_MANIFEST_FILE)):
        logger.error("Intermediate manifest file exists, cannot proceed with migration.")
        return
    if os.path.exists(os.path.join(output_dir, OLD_OBJS_FILE)):
        logger.error("Deleted objects file exists, cannot proceed with migration.")
        return
    
    # Create extra subdirectory structure and move sequence files
    for (_i, row) in manifest.iterrows():
        sample = row[SEQ_ID_KEY]
        current_dir = os.path.join(output_dir, sample)
        new_dir = os.path.join(output_dir, sample, seq_type)
        create_dir(new_dir)
        if old_seq_type == 'fastq':
            read1 = row['FASTQ_R1']
            read2 = row['FASTQ_R2']
            os.rename(os.path.join(current_dir, read1), os.path.join(new_dir, read1))
            os.rename(os.path.join(current_dir, read2), os.path.join(new_dir, read2))
        elif old_seq_type == 'fasta':
            file = row['FASTA_R1']
            os.rename(os.path.join(current_dir, file), os.path.join(new_dir, file))

    # Save updated sync state
    save_json(sync_state, get_path(sync_state, SYNC_STATE_FILE_KEY))
    # Save new manifest file with updated column names
    if old_seq_type == 'fastq':
        assert list(manifest.columns) == [
            'Seq_ID', 'FASTQ_R1', 'FASTQ_R2', 'HASH_FASTQ_R1', 'HASH_FASTQ_R2'
        ]
    elif old_seq_type == 'fasta':
        assert list(manifest.columns) == ['Seq_ID', 'FASTA_R1', 'HASH_FASTA_R1']
    manifest.columns=list_expected_headers(seq_type)
    m_path = get_path(sync_state, MANIFEST_KEY)
    save_to_csv(manifest, m_path)
    # Delete old manifest file and sync state
    os.remove(os.path.join(output_dir, OLD_SYNC_STATE_FILE))
    os.remove(os.path.join(output_dir, OLD_MANIFEST_FILE))
    # Move consensus sequences
    if old_seq_type == 'fasta':
        os.rename(
            os.path.join(output_dir, OLD_FASTA_AGGREGATE_FILE_NAME),
            os.path.join(output_dir, FASTA_AGGREGATE_FILE_NAME)
        )
    logger.success("Migration complete")
    