

from austrakka.components.sequence.funcs import _rename_fasta_asm_contigs
from io import BytesIO

input_fasta = \
""">seq1 the first sequence
ACGT
TTTT
>seq2 the second sequence
ACGT
"""

expected_transformed_fasta = \
""">Seq123.seq1 the first sequence
ACGT
TTTT
>Seq123.seq2 the second sequence
ACGT
"""

class TestSequenceFuncs:
    
    def test_fasta_asm_contig_rename(self):
        input_stream = BytesIO(input_fasta.encode('utf-8'))
        output_stream = _rename_fasta_asm_contigs(input_stream, 'Seq123')
        assert output_stream.getvalue() == expected_transformed_fasta.encode('utf-8')
        