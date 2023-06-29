# from click.testing import CliRunner
# from austrakka.main import get_cli
# from austrakka.utils.exceptions import FailedResponseException
# 
# 
# class TestSequenceCommands:
#     runner = CliRunner()
# 
#     def test_get_seq__unknown_seq_type__expect_error(self):
#         result = self.runner.invoke(get_cli(), [
#             'seq',
#             'list',
#             '-g',
#             'fake-group',
#             '-t',
#             'fastb'
#         ])
#         assert "Error: Invalid value for '-t' / '--type': 'fastb' is not one " \
#                "of 'fasta', 'fastq'." in result.output
#         assert result.exit_code == 2
# 
#     def test_get_seq__unknown_read__expect_error(self):
#         result = self.runner.invoke(get_cli(), [
#             'seq',
#             'list',
#             '-g',
#             'fake-group',
#             '-r',
#             '3'
#         ])
#         assert "Error: Invalid value for '-r' / '--read': '3' is not one of " \
#                "'1', '2', '-1'." in result.output
#         assert result.exit_code == 2
# 
#     def test_get_seq__missing_filter__expect_error(self):
#         result = self.runner.invoke(get_cli(), [
#             'seq',
#             'list'
#         ])
#         assert "Error: Either 'group' or 'analysis' must be provided"\
#                in result.output
#         assert result.exit_code == 2
# 
#     def test_get_seq__unknown_analysis__expect_error(self):
#         result = self.runner.invoke(get_cli(), [
#             'seq',
#             'list',
#             '-a',
#             'fake-analysis'
#         ])
#         assert isinstance(result.exception, FailedResponseException)
#         assert "Analysis with abbreviation fake-analysis not found" \
#                in result.exception.get_error_messages()
#         assert result.exit_code == 1
