from uuid import UUID

import pytest
import responses

from pylibrelinkup import AuthenticationError, PatientNotFoundError
from pylibrelinkup.models.data import GlucoseMeasurement
from tests.factories import PatientFactory


def test_logbook_raises_authentication_error_for_unauthenticated_client(
    pylibrelinkup_client,
):
    """Test that the logbook method raises ValueError for an unauthenticated client."""
    with pytest.raises(AuthenticationError, match="PyLibreLinkUp not authenticated"):
        pylibrelinkup_client.client.logbook(
            UUID("12345678-1234-5678-1234-567812345678")
        )


def test_logbook_returns_logbook_response_for_valid_uuid(
    mocked_responses, logbook_response_json, pylibrelinkup_client
):
    """Test that the logbook method returns LogbookResponse for a valid UUID."""
    patient_id = UUID("12345678-1234-5678-1234-567812345678")

    mocked_responses.add(
        responses.GET,
        f"{pylibrelinkup_client.api_url.value}/llu/connections/{patient_id}/logbook",
        json=logbook_response_json,
        status=200,
    )

    pylibrelinkup_client.client.token = "not_a_token"

    result = pylibrelinkup_client.client.logbook(patient_id)

    assert isinstance(result, list)
    assert all([isinstance(measurement, GlucoseMeasurement) for measurement in result])
    assert (
        result[0].value_in_mg_per_dl
        == logbook_response_json["data"][0]["ValueInMgPerDl"]
    )


def test_logbook_returns_logbook_response_for_valid_patient(
    mocked_responses, logbook_response_json, pylibrelinkup_client
):
    """Test that the logbook method returns LogbookResponse for a valid Patient."""
    patient = PatientFactory.build()

    mocked_responses.add(
        responses.GET,
        f"{pylibrelinkup_client.api_url.value}/llu/connections/{patient.patient_id}/logbook",
        json=logbook_response_json,
        status=200,
    )

    pylibrelinkup_client.client.token = "not_a_token"

    result = pylibrelinkup_client.client.logbook(patient)

    assert isinstance(result, list)
    assert all([isinstance(measurement, GlucoseMeasurement) for measurement in result])
    assert (
        result[0].value_in_mg_per_dl
        == logbook_response_json["data"][0]["ValueInMgPerDl"]
    )


def test_logbook_returns_logbook_response_for_valid_string(
    mocked_responses, logbook_response_json, pylibrelinkup_client
):
    """Test that the logbook method returns LogbookResponse for a valid string representation of a UUID."""
    patient_id = "12345678-1234-5678-1234-567812345678"

    mocked_responses.add(
        responses.GET,
        f"{pylibrelinkup_client.api_url.value}/llu/connections/{patient_id}/logbook",
        json=logbook_response_json,
        status=200,
    )

    pylibrelinkup_client.client.token = "not_a_token"

    result = pylibrelinkup_client.client.logbook(patient_id)

    assert isinstance(result, list)
    assert all([isinstance(measurement, GlucoseMeasurement) for measurement in result])
    assert (
        result[0].value_in_mg_per_dl
        == logbook_response_json["data"][0]["ValueInMgPerDl"]
    )


def test_logbook_raises_value_error_for_invalid_uuid_string(
    mocked_responses, pylibrelinkup_client
):
    """Test that the logbook method raises ValueError for an invalid UUID string."""
    pylibrelinkup_client.client.token = "not_a_token"

    with pytest.raises(ValueError, match="Invalid patient_identifier"):
        pylibrelinkup_client.client.logbook("i'm not a uuid")


def test_logbook_raises_value_error_for_invalid_patient_id_type(pylibrelinkup_client):
    """Test that the logbook method raises ValueError for an invalid patient_id type."""
    pylibrelinkup_client.client.token = "not_a_token"

    with pytest.raises(ValueError, match="Invalid patient_identifier"):
        pylibrelinkup_client.client.logbook(123456)  # type: ignore


@pytest.fixture
def logbook_response_json(get_response_json):
    return get_response_json("logbook_response.json")


def test_patient_id_not_found_raises_patient_not_found_error(
    mocked_responses, pylibrelinkup_client, get_response_json
):
    """Test that the logbook method raises PatientNotFoundError for a patient_id not found."""
    patient_id = UUID("12345678-1234-5678-1234-567812345678")

    mocked_responses.add(
        responses.GET,
        f"{pylibrelinkup_client.api_url.value}/llu/connections/{patient_id}/logbook",
        json=get_response_json("terms_of_use_response.json"),
        status=200,
    )

    pylibrelinkup_client.client.token = "not_a_token"

    with pytest.raises(PatientNotFoundError):
        pylibrelinkup_client.client.logbook(patient_id)
