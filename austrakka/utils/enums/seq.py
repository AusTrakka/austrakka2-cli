from enum import Enum
from typing import Optional

# These enum values give the strings passed to the API to specify types
# Should correspond to the server-side SequenceTypes consts
# These strings are user-facing in the CLI as subcommands or type options
class SeqType(Enum):
    FASTQ_ILL_PE = 'fastq-ill-pe'
    FASTQ_ILL_SE = 'fastq-ill-se'
    FASTQ_ONT = 'fastq-ont'
    FASTA_CNS = 'fasta-cns'
    FASTA_ASM = 'fasta-asm'


def convert_to_seq_type(seq_type: str) -> Optional[SeqType]:
    """
    Convert a string to a SeqType enum value.
    
    Args:
        seq_type: The string representation of a sequence type
        
    Returns:
        The corresponding SeqType enum value, or None if seq_type_str is None
        
    Raises:
        ValueError: If the string is empty or doesn't match any enum value
    """
    if seq_type is None:
        return None
    
    if seq_type == "":
        valid_types = [t.value for t in SeqType]
        raise ValueError(f"Sequence type cannot be empty. Valid types are: {', '.join(valid_types)}")

    try:
        return SeqType(seq_type.lower())
    except ValueError:
        valid_types = [t.value for t in SeqType]
        raise ValueError(f"Invalid sequence type '{seq_type}'. Valid types are: {', '.join(valid_types)}")


BY_IS_ACTIVE_FLAG = 'by-is-active-flag'
BY_LATEST_DATE = 'by-latest-date'

SEQ_FILTERS = [BY_IS_ACTIVE_FLAG, BY_LATEST_DATE]