from uuid import UUID

from pylibrelinkup.models.data import Patient

PatientIdentifier = UUID | str | Patient
