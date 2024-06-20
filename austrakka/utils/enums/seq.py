from enum import Enum

# These enum values give the strings passed to the API to specify types
# Should correspond to the server-side SequenceTypes consts
# These strings are user-facing in the CLI as subcommands or type options
class SeqType(Enum):
    FASTQ_ILL_PE = 'fastq-ill-pe'
    FASTA_CNS = 'fasta-cns'

BY_IS_ACTIVE_FLAG = 'by-is-active-flag'
BY_LATEST_DATE = 'by-latest-date'

SEQ_FILTERS = [BY_IS_ACTIVE_FLAG, BY_LATEST_DATE]
