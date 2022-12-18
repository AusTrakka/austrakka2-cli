from click.testing import CliRunner
from austrakka.main import get_cli
from austrakka.utils.exceptions import FailedResponseException


class TestSequenceCommands:
    runner = CliRunner()

    def test_get_seq__unknown_seq_type__expect_error(self):
        result = self.runner.invoke(get_cli(), [
            'seq',
            'list',
            '-s',
            'fake-species',
            '-t',
            'fastb'
        ])
        assert "Error: Invalid value for '-t' / '--type': 'fastb' is not one " \
               "of 'fasta', 'fastq'." in result.output
        assert result.exit_code == 2

    def test_get_seq__unknown_read__expect_error(self):
        result = self.runner.invoke(get_cli(), [
            'seq',
            'list',
            '-s',
            'fake-species',
            '-r',
            '3'
        ])
        assert "Error: Invalid value for '-r' / '--read': '3' is not one of " \
               "'1', '2', '-1'." in result.output
        assert result.exit_code == 2

    def test_get_seq__missing_filter__expect_error(self):
        result = self.runner.invoke(get_cli(), [
            'seq',
            'list'
        ])
        assert "Error: Missing one of the required mutually exclusive options "\
               "from 'Filter' " \
               'option group:\n' \
               "  '-s' / '--species'\n" \
               "  '-g' / '--group-name'\n" \
               "  '-a' / '--analysis'\n" in result.output
        assert result.exit_code == 2

    def test_get_seq__unknown_species__expect_error(self):
        result = self.runner.invoke(get_cli(), [
            'seq',
            'list',
            '-s',
            'fake-species'
        ])
        assert isinstance(result.exception, FailedResponseException)
        assert "No sequences found for species fake-species." \
               in result.exception.get_error_messages()
        assert result.exit_code == 1

    def test_get_seq__unknown_analysis__expect_error(self):
        result = self.runner.invoke(get_cli(), [
            'seq',
            'list',
            '-a',
            'fake-analysis'
        ])
        assert isinstance(result.exception, FailedResponseException)
        assert "Analysis with abbreviation fake-analysis not found" \
               in result.exception.get_error_messages()
        assert result.exit_code == 1
