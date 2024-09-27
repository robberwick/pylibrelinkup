import json
from pathlib import Path

import pytest
import responses


@pytest.fixture
def mocked_responses():
    with responses.RequestsMock() as rsps:
        yield rsps


@pytest.fixture
def graph_response_json():
    with open(Path(__file__).parent / "data" / "graph_response.json") as f:
        return json.loads(f.read())


@pytest.fixture
def terms_of_use_response_json():
    with open(Path(__file__).parent / "data" / "terms_of_use_response.json") as f:
        return json.loads(f.read())
