import json
from dataclasses import dataclass
from pathlib import Path

import pytest
import responses

from pylibrelinkup import PyLibreLinkUp, APIUrl


@pytest.fixture
def mocked_responses():
    with responses.RequestsMock() as rsps:
        yield rsps


@pytest.fixture
def graph_response_json():
    with open(Path(__file__).parent / "data" / "graph_response.json") as f:
        return json.loads(f.read())


@pytest.fixture
def graph_response_no_sd_json():
    with open(Path(__file__).parent / "data" / "graph_response_no_sd.json") as f:
        return json.loads(f.read())


@pytest.fixture
def terms_of_use_response_json():
    with open(Path(__file__).parent / "data" / "terms_of_use_response.json") as f:
        return json.loads(f.read())


@pytest.fixture
def privacy_policy_response_json():
    with open(Path(__file__).parent / "data" / "privacy_policy_response.json") as f:
        return json.loads(f.read())


@pytest.fixture
def redirect_response_json():
    with open(Path(__file__).parent / "data" / "redirect_response.json") as f:
        return json.loads(f.read())


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
