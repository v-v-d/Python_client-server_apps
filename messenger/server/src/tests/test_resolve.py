import pytest

from src.resolvers import resolve
from src.echo.controllers import echo_controller


@pytest.fixture
def action_name_fixture():
    return 'echo'


@pytest.fixture
def controller_fixture():
    return echo_controller


def test_valid_resolve(action_name_fixture, controller_fixture):
    controller = resolve(action_name_fixture)
    return controller_fixture == controller
