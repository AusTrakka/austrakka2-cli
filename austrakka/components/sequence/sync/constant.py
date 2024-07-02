# Sync state key constants
MANIFEST_KEY = 'manifest'
INTERMEDIATE_MANIFEST_FILE_KEY = 'intermediate_manifest_file'
GROUP_NAME_KEY = 'group_name'
SEQ_TYPE_KEY = 'seq_type'
OUTPUT_DIR_KEY = 'output_dir'
SYNC_STATE_FILE_KEY = 'sync_state_file'
RECALCULATE_HASH_KEY = 'recalculate_hash'
OBSOLETE_OBJECTS_FILE_KEY = 'obsolete_objects_file'
CURRENT_STATE_KEY = 'current_state'
CURRENT_ACTION_KEY = 'current_action'
TRASH_DIR_KEY = 'trash_dir'
DOWNLOAD_BATCH_SIZE_KEY = 'download_batch_size'

# File extensions
FASTQ_EXTS = ['fastq', 'fq']
FASTA_EXTS = ['fasta', 'fa']
GZ_EXT = 'gz'

# Obsolete file keys
FILE_NAME_KEY = 'file_name'
FILE_PATH_KEY = 'file_path'
DETECTION_DATE_KEY = 'detection_date'

# Intermediate manifest file keys
STATUS_KEY = 'status'
HOT_SWAP_NAME_KEY = 'hot_swap_name'
FILE_NAME_ON_DISK_KEY = 'fileNameOnDisk'
INT_FILE_NAME_KEY = 'fileName'
SAMPLE_NAME_KEY = 'sampleName'
READ_KEY = 'read'
BLOB_FILE_PATH_KEY = 'blobFilePath'
SERVER_SHA_256_KEY = 'serverSha256'
TYPE_KEY = 'type'
IS_ACTIVE_KEY = 'isActive'

# Manifest file keys
SEQ_ID_KEY = 'Seq_ID'

# Workflow value constants
DOWNLOADED = 'downloaded'
DRIFTED = 'drifted'
FAILED = 'failed'
MATCH = 'match'
MISSING = 'missing'
DONE = 'done'

# Command level value constants
# SEQTYPE will be replaced with the seq type being operated on
MANIFEST_FILE_NAME = 'manifest-SEQTYPE.csv'
FASTA_AGGREGATE_FILE_NAME = 'consensus.fasta'
INTERMEDIATE_FASTA_AGGREGATE_FILE_NAME = 'intermediate-consensus.fasta'
INTERMEDIATE_MANIFEST_FILE = 'intermediate-manifest-SEQTYPE.csv'
OBSOLETE_OBJECTS_FILE = 'delete-targets-SEQTYPE.csv'
SYNC_STATE_FILE = 'sync-state-SEQTYPE.json'
TRASH_DIR = '.trash'

# Used for migration from old sync system
OLD_SYNC_STATE_FILE = 'sync-state.json'
OLD_MANIFEST_FILE = 'manifest.csv'
OLD_OBJS_FILE = 'delete-targets.csv'
OLD_INTERMEDIATE_MANIFEST_FILE = 'intermediate-manifest.csv'
OLD_FASTA_AGGREGATE_FILE_NAME = 'all.fasta'
MIGRATE_SEQ_TYPES = {
    'fastq': 'fastq-ill-pe',
    'fasta': 'fasta-cns'
}
