import json
from dataclasses import dataclass
from pathlib import Path

import pytest
import responses

from pylibrelinkup import APIUrl, PyLibreLinkUp


@pytest.fixture
def mocked_responses():
    with responses.RequestsMock() as rsps:
        yield rsps


@pytest.fixture
def get_response_json():
    def _load_json(filename: str) -> dict:
        with open(Path(__file__).parent / "data" / filename) as f:
            return json.loads(f.read())

    return _load_json


@pytest.fixture
def graph_response_json(get_response_json):
    return get_response_json("graph_response.json")


@pytest.fixture
def graph_response_no_sd_json(get_response_json):
    return get_response_json("graph_response_no_sd.json")


@pytest.fixture
def graph_response_no_alarm_rules_c_json(get_response_json):
    return get_response_json("graph_response_no_alarm_rules_c.json")


@pytest.fixture
def graph_response_no_u_json(get_response_json):
    return get_response_json("graph_response_no_u.json")


@dataclass
class PyLibreLinkUpClientFixture:
    client: PyLibreLinkUp
    api_url: APIUrl


@pytest.fixture(params=APIUrl)
def api_url(request) -> APIUrl:
    return request.param


@pytest.fixture()
def pylibrelinkup_client(api_url: APIUrl) -> PyLibreLinkUpClientFixture:
    return PyLibreLinkUpClientFixture(
        client=PyLibreLinkUp(email="parp", password="parp", api_url=api_url),
        api_url=api_url,
    )
