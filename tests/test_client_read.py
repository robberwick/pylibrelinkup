from uuid import UUID

import pytest
import responses

from pylibrelinkup import PyLibreLinkUp, APIUrl, AuthenticationError, ConnectionResponse
from tests.conftest import graph_response_json
from tests.factories import PatientFactory


def test_read_raises_authentication_error_for_unauthenticated_client(
    pylibrelinkup_client,
):
    """Test that the read method raises ValueError for an unauthenticated client."""
    with pytest.raises(AuthenticationError, match="PyLibreLinkUp not authenticated"):
        pylibrelinkup_client.client.read(UUID("12345678-1234-5678-1234-567812345678"))


def test_read_returns_connection_response_for_valid_uuid(
    mocked_responses, graph_response_json, pylibrelinkup_client
):
    """Test that the read method returns ConnectionResponse for a valid UUID."""
    patient_id = UUID("12345678-1234-5678-1234-567812345678")

    mocked_responses.add(
        responses.GET,
        f"{pylibrelinkup_client.api_url.value}/llu/connections/{patient_id}/graph",
        json=graph_response_json,
        status=200,
    )

    pylibrelinkup_client.client.token = "not_a_token"

    result = pylibrelinkup_client.client.read(patient_id)

    assert isinstance(result, ConnectionResponse)
    assert (
        str(result.data.connection.id)
        == graph_response_json["data"]["connection"]["id"]
    )


def test_read_returns_connection_response_for_valid_patient(
    mocked_responses, graph_response_json, pylibrelinkup_client
):
    """Test that the read method returns ConnectionResponse for a valid Patient."""
    patient = PatientFactory.build()

    mocked_responses.add(
        responses.GET,
        f"{pylibrelinkup_client.api_url.value}/llu/connections/{patient.patient_id}/graph",
        json=graph_response_json,
        status=200,
    )

    pylibrelinkup_client.client.token = "not_a_token"

    result = pylibrelinkup_client.client.read(patient)

    assert isinstance(result, ConnectionResponse)
    assert (
        str(result.data.connection.id)
        == graph_response_json["data"]["connection"]["id"]
    )


def test_read_returns_connection_response_for_valid_string(
    mocked_responses, graph_response_json, pylibrelinkup_client
):
    """Test that the read method returns ConnectionResponse for a valid string representation of a UUID."""
    patient_id = "12345678-1234-5678-1234-567812345678"

    mocked_responses.add(
        responses.GET,
        f"{pylibrelinkup_client.api_url.value}/llu/connections/{patient_id}/graph",
        json=graph_response_json,
        status=200,
    )

    pylibrelinkup_client.client.token = "not_a_token"

    result = pylibrelinkup_client.client.read(patient_id)

    assert isinstance(result, ConnectionResponse)
    assert (
        str(result.data.connection.id)
        == graph_response_json["data"]["connection"]["id"]
    )


def test_read_raises_value_error_for_invalid_uuid_string(
    mocked_responses, pylibrelinkup_client
):
    """Test that the read method raises ValueError for an invalid UUID string."""
    pylibrelinkup_client.client.token = "not_a_token"

    with pytest.raises(ValueError, match="Invalid patient_identifier"):
        pylibrelinkup_client.client.read("i'm not a uuid")


def test_read_raises_value_error_for_invalid_patient_id_type(pylibrelinkup_client):
    """Test that the read method raises ValueError for an invalid patient_id type."""
    pylibrelinkup_client.client.token = "not_a_token"

    with pytest.raises(ValueError, match="Invalid patient_identifier"):
        pylibrelinkup_client.client.read(123456)  # type: ignore


def test_read_response_no_sd_returns_connection_response(
    mocked_responses, graph_response_no_sd_json, pylibrelinkup_client
):
    """Test that the read method returns ConnectionResponse when no sd key is present in llu api response data."""
    patient_id = UUID("12345678-1234-5678-1234-567812345678")

    mocked_responses.add(
        responses.GET,
        f"{pylibrelinkup_client.api_url.value}/llu/connections/{patient_id}/graph",
        json=graph_response_no_sd_json,
        status=200,
    )

    pylibrelinkup_client.client.token = "not_a_token"

    result = pylibrelinkup_client.client.read(patient_id)

    assert isinstance(result, ConnectionResponse)
    assert (
        str(result.data.connection.id)
        == graph_response_no_sd_json["data"]["connection"]["id"]
    )
