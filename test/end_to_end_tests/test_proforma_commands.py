import pytest
import json
from click.testing import Result

from ete_cmd_bricks import _create_min_proforma, _create_field_if_not_exists
from ete_utils import _new_identifier
from test.utils.austrakka_test_cli import AusTrakkaTestCli


class TestProformaCommands:
    @pytest.fixture(autouse=True)
    def _use_cli(self, austrakka_test_cli: AusTrakkaTestCli):
        self.cli = austrakka_test_cli

    def _get_proforma_fields(self, proforma_name: str):
        result: Result = self.cli.invoke([
            'proforma',
            'show',
            proforma_name,
            '--format',
            'json'
        ])
        return json.loads(result.output)

    def test_add_version_no_op_when_spec_is_identical(self):
        # Arrange
        proforma_name = f'pf-{_new_identifier(10)}'
        _create_min_proforma(self.cli, proforma_name)

        # Act
        result: Result = self.cli.invoke([
            'proforma',
            'add-version',
            proforma_name,
            '--inherit',
        ])

        # Assert
        assert result.exit_code == 0
        assert "The specified pro forma fields are identical to the current version." in result.output

    def test_add_version_with_inherit_and_add_required_field(self):
        # Arrange
        proforma_name = f'pf-{_new_identifier(10)}'
        _create_min_proforma(self.cli, proforma_name)
        new_field = f'req-{_new_identifier(10)}'
        _create_field_if_not_exists(self.cli, new_field)

        # Act
        result: Result = self.cli.invoke([
            'proforma',
            'add-version',
            proforma_name,
            '--inherit',
            '--required-field',
            new_field,
        ])

        # Assert
        assert result.exit_code == 0
        fields = self._get_proforma_fields(proforma_name)
        field_names = [field['name'] for field in fields]
        assert new_field in field_names
        new_field_data = next(field for field in fields if field['name'] == new_field)
        assert new_field_data['isRequired'] is True

    def test_add_version_with_inherit_and_add_optional_field(self):
        # Arrange
        proforma_name = f'pf-{_new_identifier(10)}'
        _create_min_proforma(self.cli, proforma_name)
        new_field = f'opt-{_new_identifier(10)}'
        _create_field_if_not_exists(self.cli, new_field)

        # Act
        result: Result = self.cli.invoke([
            'proforma',
            'add-version',
            proforma_name,
            '--inherit',
            '--optional-field',
            new_field,
        ])

        # Assert
        assert result.exit_code == 0
        fields = self._get_proforma_fields(proforma_name)
        field_names = [field['name'] for field in fields]
        assert new_field in field_names
        new_field_data = next(field for field in fields if field['name'] == new_field)
        assert new_field_data['isRequired'] is False

    def test_add_version_with_inherit_and_remove_field(self):
        # Arrange
        field_to_remove = f'rm-{_new_identifier(10)}'
        proforma_name = f'pf-{_new_identifier(10)}'
        _create_min_proforma(self.cli, proforma_name, required_fields=[field_to_remove])

        # Act
        result: Result = self.cli.invoke([
            'proforma',
            'add-version',
            proforma_name,
            '--inherit',
            '-rm',
            field_to_remove,
        ])

        # Assert
        assert result.exit_code == 0
        fields = self._get_proforma_fields(proforma_name)
        field_names = [field['name'] for field in fields]
        assert field_to_remove not in field_names

    def test_add_version_without_inherit(self):
        # Arrange
        custom_field = f'custom-{_new_identifier(10)}'
        proforma_name = f'pf-{_new_identifier(10)}'
        _create_min_proforma(self.cli, proforma_name, required_fields=[custom_field])
        new_field = f'only-{_new_identifier(10)}'
        _create_field_if_not_exists(self.cli, new_field)

        # Act
        result: Result = self.cli.invoke([
            'proforma',
            'add-version',
            proforma_name,
            '--required-field',
            new_field,
        ])

        # Assert
        assert result.exit_code == 0
        fields = self._get_proforma_fields(proforma_name)
        field_names = [field['name'] for field in fields]
        assert new_field in field_names
        assert custom_field not in field_names # Should not be inherited
        assert 'Seq_ID' in field_names # System field should still be there

    def test_add_version_change_field_from_required_to_optional(self):
        # Arrange
        field_to_change = f'req-to-opt-{_new_identifier(10)}'
        proforma_name = f'pf-{_new_identifier(10)}'
        _create_min_proforma(self.cli, proforma_name, required_fields=[field_to_change])

        # Act
        result: Result = self.cli.invoke([
            'proforma',
            'add-version',
            proforma_name,
            '--inherit',
            '--optional-field',
            field_to_change,
        ])

        # Assert
        assert result.exit_code == 0
        fields = self._get_proforma_fields(proforma_name)
        field_data = next(field for field in fields if field['name'] == field_to_change)
        assert field_data['isRequired'] is False

    def test_add_version_change_field_from_optional_to_required(self):
        # Arrange
        field_to_change = f'opt-to-req-{_new_identifier(10)}'
        proforma_name = f'pf-{_new_identifier(10)}'
        _create_min_proforma(self.cli, proforma_name, optional_fields=[field_to_change])

        # Act
        result: Result = self.cli.invoke([
            'proforma',
            'add-version',
            proforma_name,
            '--inherit',
            '--required-field',
            field_to_change,
        ])

        # Assert
        assert result.exit_code == 0
        fields = self._get_proforma_fields(proforma_name)
        field_data = next(field for field in fields if field['name'] == field_to_change)
        assert field_data['isRequired'] is True

    def test_add_version_should_raise_error_on_conflicting_required_and_optional(self):
        # Arrange
        proforma_name = f'pf-{_new_identifier(10)}'
        _create_min_proforma(self.cli, proforma_name)
        conflicting_field = f'conflict-{_new_identifier(10)}'
        _create_field_if_not_exists(self.cli, conflicting_field)

        # Act
        result: Result = self.cli.invoke([
            'proforma',
            'add-version',
            proforma_name,
            '--required-field',
            conflicting_field,
            '--optional-field',
            conflicting_field,
        ])

        # Assert
        assert result.exit_code != 0
        assert isinstance(result.exception, ValueError)
        assert 'The following fields have been specified as both required and optional' in str(result.exception)

    def test_add_version_should_raise_error_on_conflicting_remove_and_add(self):
        # Arrange
        proforma_name = f'pf-{_new_identifier(10)}'
        _create_min_proforma(self.cli, proforma_name)
        conflicting_field = f'conflict-{_new_identifier(10)}'
        _create_field_if_not_exists(self.cli, conflicting_field)

        # Act
        result: Result = self.cli.invoke([
            'proforma',
            'add-version',
            proforma_name,
            '--required-field',
            conflicting_field,
            '-rm',
            conflicting_field,
        ])

        # Assert
        assert result.exit_code != 0
        assert isinstance(result.exception, ValueError)
        assert 'The following fields have been specified as both to be added/updated and removed' in str(result.exception)

    def test_add_version_should_warn_when_removing_non_existent_field(self):
        # Arrange
        proforma_name = f'pf-{_new_identifier(10)}'
        _create_min_proforma(self.cli, proforma_name)
        non_existent_field = f'non-existent-{_new_identifier(10)}'

        # Act
        result: Result = self.cli.invoke([
            'proforma',
            'add-version',
            proforma_name,
            '--inherit',
            '-rm',
            non_existent_field,
        ])

        # Assert
        assert result.exit_code == 0
        assert f"Field 'f{non_existent_field}' specified for removal was not found" in result.output

    def test_add_version_should_raise_error_on_removing_system_field(self):
        # Arrange
        proforma_name = f'pf-{_new_identifier(10)}'
        _create_min_proforma(self.cli, proforma_name)
        field_to_remove = 'Seq_ID'

        # Act
        result: Result = self.cli.invoke([
            'proforma',
            'add-version',
            proforma_name,
            '--inherit',
            '-rm',
            field_to_remove,
        ])

        # Assert
        assert result.exit_code != 0
        assert isinstance(result.exception, ValueError)
        assert 'The following system fields cannot be removed' in str(result.exception)