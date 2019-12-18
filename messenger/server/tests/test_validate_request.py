import pytest

from protocol import validate_request


@pytest.fixture
def raw_fixture():
    return '''
        {
            "action": "echo",
            "time": 1576455201.819919,
            "data": "message",
        }
    '''


def test_valid_validate_request(raw_fixture):
    assert validate_request(raw_fixture)
