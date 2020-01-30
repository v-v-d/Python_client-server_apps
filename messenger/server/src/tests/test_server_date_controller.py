import pytest
from datetime import datetime

from src.serverdate.controllers import server_date_controller


@pytest.fixture
def action_fixture():
    return 'serverdate'


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


def test_valid_server_date_controller(request_fixture, time_fixture):
    response = server_date_controller(request_fixture)
    return response.get('time') == time_fixture
