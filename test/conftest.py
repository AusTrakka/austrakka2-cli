import pathlib
from test.utils.austrakka_test_cli import AusTrakkaTestCli
import pytest

from austrakka.main import get_cli


def pytest_collection_modifyitems(config, items):
    """
    We are using this function to add a pytest marker to all tests based
    on the top level directory they are placed under in `tests/`.
    Eg. `tests/unit_tests` will be given the marker `unit`
    """
    rootdir = pathlib.Path(config.rootdir)
    for item in items:
        rel_path = pathlib.Path(item.fspath).relative_to(rootdir)
        mark_name = next(
            (part for part in rel_path.parts if part.endswith('_tests')),
            '').removesuffix('_tests')
        if mark_name:
            mark = getattr(pytest.mark, mark_name)
            item.add_marker(mark)


def pytest_configure(config):
    """
    pytest will give a warning if we use non-registered markers.
    Here we are adding markers dynamically based on the test directories
    """
    rootdir = pathlib.Path(config.rootdir)
    for dir_ in rootdir.rglob('*_tests'):
        mark_name = dir_.stem.removesuffix('_tests')
        config.addinivalue_line('markers', mark_name)


@pytest.fixture()
def austrakka_test_cli():
    """
    Access the AusTrakka CLI in a test.
    """
    return AusTrakkaTestCli(get_cli())
