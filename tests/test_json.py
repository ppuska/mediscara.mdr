
import pytest
from pytest import FixtureRequest
import requests

from mdr import json

SERVER_URL = "http://localhost:1026"

@pytest.fixture(autouse=True)
def skip_no_connection(request: FixtureRequest):
    """Add a custom marker to pytest to skip the test if there is no connection to the OCB"""
    if request.node.get_closest_marker('skip_if_no_connection'):
        try:
            requests.get(f"{SERVER_URL}/v2", timeout=1)

        except ConnectionError:
            pytest.skip(f'No connection to server at {SERVER_URL}, skipping test')

        except requests.exceptions.ConnectTimeout:
            pytest.skip(f'No connection to server at {SERVER_URL}, skipping test')


@pytest.mark.skip_if_no_connection()
def test_json():
    """Test the JSON module"""
    json.init("http://localhost:1026")

    pdf = json.get_next_pdf()

    print(pdf)