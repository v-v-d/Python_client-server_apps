import pytest
from datetime import datetime

from src.servererrors import server_error_controller


@pytest.fixture
def action_fixture():
    return 'servererror'


@pytest.fixture
def time_fixture():
    return datetime.now().timestamp()


@pytest.fixture
def data_fixture():
    return ''


@pytest.fixture
def request_fixture():
    return {
        'action': action_fixture,
        'time': time_fixture,
        'data': data_fixture,
    }


@pytest.fixture
def error_fixture():
    return 'Server error message'


def test_valid_server_date_controller(request_fixture, error_fixture):
    try:
        response = server_error_controller(request_fixture)
    except Exception as error:
        response = error
    return response == error_fixture
