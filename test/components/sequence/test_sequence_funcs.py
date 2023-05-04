import pytest

from austrakka.components.sequence.funcs import _filter_sequences
from austrakka.components.sequence.funcs import _get_seq_api
from austrakka.utils.enums.seq import FASTA_UPLOAD_TYPE
from austrakka.utils.enums.seq import FASTQ_UPLOAD_TYPE


class TestSequenceFuncs:
    sequence_data = [
        {
            'type': 'fasta',
            'read': 1,
        },
        {
            'type': 'fasta',
            'read': 2,
        },
        {
            'type': 'fastq',
            'read': 1,
        },
        {
            'type': 'fastq',
            'read': 2,
        },
    ]

    def test_filter_sequences__read_1_fastq__expect_read_1_fastq(self):
        filtered = _filter_sequences(
            self.sequence_data,
            FASTQ_UPLOAD_TYPE,
            '1'
        )
        assert any(filtered)
        assert all(x['type'] == FASTQ_UPLOAD_TYPE for x in filtered)
        assert all(x['read'] == 1 for x in filtered)

    def test_filter_sequences__read_2_fastq__expect_read_2_fastq(self):
        filtered = _filter_sequences(
            self.sequence_data,
            FASTQ_UPLOAD_TYPE,
            '2'
        )
        assert any(filtered)
        assert all(x['type'] == FASTQ_UPLOAD_TYPE for x in filtered)
        assert all(x['read'] == 2 for x in filtered)

    def test_filter_sequences__read_both_fastq__expect_both_fastq(self):
        filtered = _filter_sequences(
            self.sequence_data,
            FASTQ_UPLOAD_TYPE,
            '-1'
        )
        assert any(filtered)
        assert all(x['type'] == FASTQ_UPLOAD_TYPE for x in filtered)
        assert any(x['read'] == 1 for x in filtered)
        assert any(x['read'] == 2 for x in filtered)

    def test_filter_sequences__read_1_fasta__expect_ignore_read(self):
        filtered = _filter_sequences(
            self.sequence_data,
            FASTA_UPLOAD_TYPE,
            '1'
        )
        assert any(filtered)
        assert all(x['type'] == FASTA_UPLOAD_TYPE for x in filtered)

    def test_filter_sequences__read_2_fasta__expect_ignore_read(self):
        filtered = _filter_sequences(
            self.sequence_data,
            FASTA_UPLOAD_TYPE,
            '2'
        )
        assert any(filtered)
        assert all(x['type'] == FASTA_UPLOAD_TYPE for x in filtered)

    def test_filter_sequences__read_both_fasta__expect_ignore_read(self):
        filtered = _filter_sequences(
            self.sequence_data,
            FASTA_UPLOAD_TYPE,
            '-1'
        )
        assert any(filtered)
        assert all(x['type'] == FASTA_UPLOAD_TYPE for x in filtered)

    def test_get_seq_api__pass_group__expect_group_path(self):
        api_path = _get_seq_api('test-group', None)
        assert api_path == 'Sequence/by-group/test-group'

    def test_get_seq_api__pass_none_params__expect_value_error(self):
        with pytest.raises(ValueError) as ex:
            _ = _get_seq_api(None, None)
        assert 'A filter has not been passed' in str(ex.value)
