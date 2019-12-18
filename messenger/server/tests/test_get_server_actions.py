import pytest

from settings import INSTALLED_MODULES
from resolvers import get_server_actions


@pytest.fixture
def installed_modules_fixture():
    return INSTALLED_MODULES


def test_valid_get_server_actions(installed_modules_fixture):
    server_actions = get_server_actions()
    server_actions_names = [name for name in server_actions]
    return installed_modules_fixture == server_actions_names
