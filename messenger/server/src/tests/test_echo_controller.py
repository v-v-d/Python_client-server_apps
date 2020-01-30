import pytest
from datetime import datetime

from src.echo.controllers import echo_controller


@pytest.fixture
def action_fixture():
    return 'echo'


@pytest.fixture
def time_fixture():
    return datetime.now().timestamp()


@pytest.fixture
def data_fixture():
    return 'message'


@pytest.fixture
def request_fixture():
    return {
        'action': action_fixture,
        'time': time_fixture,
        'data': data_fixture,
    }


def test_valid_echo_controller(request_fixture, action_fixture, time_fixture, data_fixture):
    response = echo_controller(request_fixture)
    return response.get('action') == action_fixture and \
           response.get('data') == data_fixture and \
           response.get('time') == time_fixture
