from uuid import UUID

import pytest
import responses

from pylibrelinkup import AuthenticationError, PatientNotFoundError
from pylibrelinkup.models.data import GlucoseMeasurementWithTrend, Trend
from tests.conftest import graph_response_json
from tests.factories import PatientFactory


def test_latest_raises_authentication_error_for_unauthenticated_client(
    pylibrelinkup_client,
):
    """Test that the read method raises ValueError for an unauthenticated client."""
    with pytest.raises(AuthenticationError, match="PyLibreLinkUp not authenticated"):
        pylibrelinkup_client.client.latest(UUID("12345678-1234-5678-1234-567812345678"))


def test_latest_returns_glucose_measurement_for_valid_uuid(
    mocked_responses, graph_response_json, pylibrelinkup_client
):
    """Test that the read method returns GraphResponse for a valid UUID."""
    patient_id = UUID("12345678-1234-5678-1234-567812345678")

    mocked_responses.add(
        responses.GET,
        f"{pylibrelinkup_client.api_url.value}/llu/connections/{patient_id}/graph",
        json=graph_response_json,
        status=200,
    )

    pylibrelinkup_client.client.token = "not_a_token"

    result = pylibrelinkup_client.client.latest(patient_id)

    assert isinstance(result, GlucoseMeasurementWithTrend)

    assert (
        result.value_in_mg_per_dl
        == graph_response_json["data"]["connection"]["glucoseMeasurement"][
            "ValueInMgPerDl"
        ]
    )
    assert result.trend == Trend.STABLE


def test_latest_returns_glucose_measurement_for_valid_patient(
    mocked_responses, graph_response_json, pylibrelinkup_client
):
    """Test that the read method returns GraphResponse for a valid Patient."""
    patient = PatientFactory.build()

    mocked_responses.add(
        responses.GET,
        f"{pylibrelinkup_client.api_url.value}/llu/connections/{patient.patient_id}/graph",
        json=graph_response_json,
        status=200,
    )

    pylibrelinkup_client.client.token = "not_a_token"

    result = pylibrelinkup_client.client.latest(patient)

    assert isinstance(result, GlucoseMeasurementWithTrend)

    assert (
        result.value_in_mg_per_dl
        == graph_response_json["data"]["connection"]["glucoseMeasurement"][
            "ValueInMgPerDl"
        ]
    )
    assert result.trend == Trend.STABLE


def test_latest_returns_glucose_measurement_for_valid_string(
    mocked_responses, graph_response_json, pylibrelinkup_client
):
    """Test that the read method returns GraphResponse for a valid string representation of a UUID."""
    patient_id = "12345678-1234-5678-1234-567812345678"

    mocked_responses.add(
        responses.GET,
        f"{pylibrelinkup_client.api_url.value}/llu/connections/{patient_id}/graph",
        json=graph_response_json,
        status=200,
    )

    pylibrelinkup_client.client.token = "not_a_token"

    result = pylibrelinkup_client.client.latest(patient_id)

    assert isinstance(result, GlucoseMeasurementWithTrend)

    assert (
        result.value_in_mg_per_dl
        == graph_response_json["data"]["connection"]["glucoseMeasurement"][
            "ValueInMgPerDl"
        ]
    )
    assert result.trend == Trend.STABLE


def test_latest_raises_value_error_for_invalid_uuid_string(
    mocked_responses, pylibrelinkup_client
):
    """Test that the read method raises ValueError for an invalid UUID string."""
    pylibrelinkup_client.client.token = "not_a_token"

    with pytest.raises(ValueError, match="Invalid patient_identifier"):
        pylibrelinkup_client.client.latest("i'm not a uuid")


def test_latest_raises_value_error_for_invalid_patient_id_type(pylibrelinkup_client):
    """Test that the read method raises ValueError for an invalid patient_id type."""
    pylibrelinkup_client.client.token = "not_a_token"

    with pytest.raises(ValueError, match="Invalid patient_identifier"):
        pylibrelinkup_client.client.latest(123456)  # type: ignore


def test_latest_response_no_sd_returns_glucose_measurement(
    mocked_responses, graph_response_no_sd_json, pylibrelinkup_client
):
    """Test that the read method returns GraphResponse when no sd key is present in llu api response data."""
    patient_id = UUID("12345678-1234-5678-1234-567812345678")

    mocked_responses.add(
        responses.GET,
        f"{pylibrelinkup_client.api_url.value}/llu/connections/{patient_id}/graph",
        json=graph_response_no_sd_json,
        status=200,
    )

    pylibrelinkup_client.client.token = "not_a_token"

    result = pylibrelinkup_client.client.latest(patient_id)

    assert isinstance(result, GlucoseMeasurementWithTrend)

    assert (
        result.value_in_mg_per_dl
        == graph_response_no_sd_json["data"]["connection"]["glucoseMeasurement"][
            "ValueInMgPerDl"
        ]
    )
    assert result.trend == Trend.STABLE


def test_latest_response_no_alarm_rules_c_returns_glucose_measurement(
    mocked_responses, graph_response_no_alarm_rules_c_json, pylibrelinkup_client
):
    """Test that the read method returns GraphResponse when no alarm_rules.c key is present in llu api response data."""
    patient_id = UUID("12345678-1234-5678-1234-567812345678")

    mocked_responses.add(
        responses.GET,
        f"{pylibrelinkup_client.api_url.value}/llu/connections/{patient_id}/graph",
        json=graph_response_no_alarm_rules_c_json,
        status=200,
    )

    pylibrelinkup_client.client.token = "not_a_token"

    result = pylibrelinkup_client.client.latest(patient_id)

    assert isinstance(result, GlucoseMeasurementWithTrend)
    assert (
        result.value_in_mg_per_dl
        == graph_response_no_alarm_rules_c_json["data"]["connection"][
            "glucoseMeasurement"
        ]["ValueInMgPerDl"]
    )
    assert result.trend == Trend.STABLE


def test_latest_patient_not_found_raises_patient_not_found_error(
    mocked_responses, pylibrelinkup_client, get_response_json
):
    """Test that the read method raises PatientNotFoundError for a patient not found."""
    patient_id = UUID("12345678-1234-5678-1234-567812345678")

    mocked_responses.add(
        responses.GET,
        f"{pylibrelinkup_client.api_url.value}/llu/connections/{patient_id}/graph",
        json=get_response_json("terms_of_use_response.json"),
        status=200,
    )

    pylibrelinkup_client.client.token = "not_a_token"

    with pytest.raises(
        PatientNotFoundError, match="Patient not found"
    ):  # PatientNotFoundError is a ValueError
        pylibrelinkup_client.client.latest(patient_id)
