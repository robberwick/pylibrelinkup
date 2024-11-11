from polyfactory.factories.pydantic_factory import ModelFactory

from pylibrelinkup.models.connection import GraphResponse
from pylibrelinkup.models.data import Patient
from pylibrelinkup.models.login import LoginResponse


class LoginResponseFactory(ModelFactory[LoginResponse]):
    __model__ = LoginResponse


class ConnectionResponseFactory(ModelFactory[GraphResponse]):
    __model__ = GraphResponse


class PatientFactory(ModelFactory[Patient]):
    __model__ = Patient
