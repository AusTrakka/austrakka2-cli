import pytest

from ete_utils import _new_identifier
from test.utils.austrakka_test_cli import AusTrakkaTestCli


class TestRoleRemoveCommand:
    @pytest.fixture(autouse=True)
    def _use_cli(self, austrakka_test_cli: AusTrakkaTestCli):
        self.cli = austrakka_test_cli

    def test_role_remove__given_role_exists_and_not_in_use__expect_success(self):
        # Arrange
        role_name = f'test-role-{_new_identifier(10)}'
        _create_role(self.cli, role_name)
        
        # Verify role was created
        assert _role_exists(self.cli, role_name), f'Role {role_name} should exist before removal'
        
        # Act
        result = self.cli.invoke([
            'iam',
            'role',
            'remove',
            '-r', role_name,
            '--no-confirm'
        ])
        
        # Assert
        assert result.exit_code == 0, f'Failed to remove role {role_name}: {result.output}'
        assert not _role_exists(self.cli, role_name), f'Role {role_name} should not exist after removal'


def _create_role(cli: AusTrakkaTestCli, role_name: str):
    """Create a role for testing purposes"""
    result = cli.invoke([
        'iam',
        'role',
        'add',
        '-r', role_name,
        '-d', f'Test role {role_name}',
        '-pv', 'User'
    ])
    assert result.exit_code == 0, f'Failed to create role {role_name} as part of test setup: {result.output}'


def _role_exists(cli: AusTrakkaTestCli, role_name: str) -> bool:
    """Check if a role exists by attempting to list roles and parsing output"""
    result = cli.invoke([
        'iam',
        'role',
        'list',
        '-f', 'json'
    ])
    if result.exit_code != 0:
        return False
    
    # Parse JSON output to check if role exists
    import json
    try:
        roles_data = json.loads(result.output)
        if isinstance(roles_data, list):
            return any(role.get('name') == role_name for role in roles_data)
        elif isinstance(roles_data, dict) and 'data' in roles_data:
            return any(role.get('name') == role_name for role in roles_data['data'])
    except (json.JSONDecodeError, KeyError):
        pass
    return False