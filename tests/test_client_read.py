from uuid import UUID

import pytest
import responses

from pylibrelinkup.api_url import APIUrl
from pylibrelinkup.client import Client
from pylibrelinkup.models.connection import ConnectionResponse
from tests.conftest import graph_response_json
from tests.factories import PatientFactory


def test_read_returns_connection_response_for_valid_uuid(
    mocked_responses, graph_response_json
):
    """Test that the read method returns ConnectionResponse for a valid UUID."""
    patient_id = UUID("12345678-1234-5678-1234-567812345678")

    mocked_responses.add(
        responses.GET,
        f"{APIUrl.US.value}/llu/connections/{patient_id}/graph",
        json=graph_response_json,
        status=200,
    )

    client = Client(email="parp", password="parp", api_url=APIUrl.US)

    result = client.read(patient_id)

    assert isinstance(result, ConnectionResponse)
    assert (
        str(result.data.connection.id)
        == graph_response_json["data"]["connection"]["id"]
    )


def test_read_returns_connection_response_for_valid_patient(
    mocked_responses, graph_response_json
):
    """Test that the read method returns ConnectionResponse for a valid Patient."""
    patient = PatientFactory.build()

    mocked_responses.add(
        responses.GET,
        f"{APIUrl.US.value}/llu/connections/{patient.patient_id}/graph",
        json=graph_response_json,
        status=200,
    )

    client = Client(email="parp", password="parp", api_url=APIUrl.US)

    result = client.read(patient)

    assert isinstance(result, ConnectionResponse)
    assert (
        str(result.data.connection.id)
        == graph_response_json["data"]["connection"]["id"]
    )


def test_read_returns_connection_response_for_valid_string(
    mocked_responses, graph_response_json
):
    """Test that the read method returns ConnectionResponse for a valid string representation of a UUID."""
    patient_id = "12345678-1234-5678-1234-567812345678"

    mocked_responses.add(
        responses.GET,
        f"{APIUrl.US.value}/llu/connections/{patient_id}/graph",
        json=graph_response_json,
        status=200,
    )

    client = Client(email="parp", password="parp", api_url=APIUrl.US)

    result = client.read(patient_id)

    assert isinstance(result, ConnectionResponse)
    assert (
        str(result.data.connection.id)
        == graph_response_json["data"]["connection"]["id"]
    )


def test_read_raises_value_error_for_invalid_uuid_string(mocked_responses):
    """Test that the read method raises ValueError for an invalid UUID string."""
    client = Client(email="parp", password="parp", api_url=APIUrl.US)

    with pytest.raises(ValueError, match="Invalid patient_identifier"):
        client.read("i'm not a uuid")


def test_read_raises_value_error_for_invalid_patient_id_type():
    """Test that the read method raises ValueError for an invalid patient_id type."""
    client = Client(email="parp", password="parp", api_url=APIUrl.EU2)

    with pytest.raises(ValueError, match="Invalid patient_identifier"):
        client.read(123456)
