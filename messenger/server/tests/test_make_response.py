import pytest
from datetime import datetime

from protocol import make_response


@pytest.fixture
def action_fixture():
    return 'test_action'


@pytest.fixture
def time_fixture():
    return datetime.now().timestamp()


@pytest.fixture
def data_fixture():
    return datetime.now().timestamp()


@pytest.fixture
def code_fixture():
    return 200


@pytest.fixture
def request_fixture():
    return {
        'action': action_fixture,
        'time': time_fixture,
        'data': data_fixture,
    }


def test_valid_make_response(request_fixture, code_fixture, data_fixture):
    response = make_response(request_fixture, code_fixture, data_fixture)
    assert response.get('code') == code_fixture
