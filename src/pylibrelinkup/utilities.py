from __future__ import annotations

from uuid import UUID

from pylibrelinkup.models.data import Patient


def coerce_patient_id(patient_identifier):
    invalid_patient_identifier = "Invalid patient_identifier"
    patient_id: UUID | None = None
    if isinstance(patient_identifier, UUID):
        patient_id = patient_identifier
    elif isinstance(patient_identifier, str):
        try:
            patient_id = UUID(patient_identifier)
        except ValueError as exc:
            raise ValueError(invalid_patient_identifier) from exc
    elif isinstance(patient_identifier, Patient):
        patient_id = patient_identifier.patient_id
    else:
        raise ValueError(invalid_patient_identifier)
    return patient_id
