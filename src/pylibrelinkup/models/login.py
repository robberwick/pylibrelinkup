from typing import List

from pydantic import Field

from .base import ConfigBaseModel

__all__ = [
    "Llu",
    "Consents",
    "SystemMessages",
    "System",
    "User",
    "Notifications",
    "DataMessages",
    "AuthTicket",
    "Data",
    "LoginResponse",
    "ErrorMessage",
    "LoginResponseUnauthenticated",
    "LoginRedirectData",
    "LoginRedirectResponse",
    "LoginArgs",
]


class Llu(ConfigBaseModel):
    policyAccept: int = Field(default=0)
    touAccept: int = Field(default=0)


class HistoryItem(ConfigBaseModel):
    policyAccept: int = Field(default=0)
    declined: bool | None = None


class RealWorldEvidence(ConfigBaseModel):
    policyAccept: int = Field(default=0)
    declined: bool = False
    touAccept: int = Field(default=0)
    history: List[HistoryItem] = []


class Consents(ConfigBaseModel):
    llu: Llu = Llu()
    realWorldEvidence: RealWorldEvidence = RealWorldEvidence()


class SystemMessages(ConfigBaseModel):
    firstUsePhoenix: int = Field(default=0)
    firstUsePhoenixReportsDataMerged: int = Field(default=0)
    lluGettingStartedBanner: int = Field(default=0)
    lluNewFeatureModal: int = Field(default=0)
    lluOnboarding: int = Field(default=0)
    lvWebPostRelease: str = Field(default="")


class System(ConfigBaseModel):
    messages: SystemMessages


class User(ConfigBaseModel):
    id: str = Field(default="")
    firstName: str = Field(default="")
    lastName: str = Field(default="")
    email: str = Field(default="")
    country: str = Field(default="")
    uiLanguage: str = Field(default="")
    communicationLanguage: str = Field(default="")
    accountType: str = Field(default="")
    uom: str = Field(default="")
    dateFormat: str = Field(default="")
    timeFormat: str = Field(default="")
    emailDay: List[int]
    system: System
    details: dict
    created: int
    lastLogin: int
    programs: dict
    dateOfBirth: int
    practices: dict
    devices: dict
    consents: Consents


class Notifications(ConfigBaseModel):
    unresolved: int = Field(default=0)


class DataMessages(ConfigBaseModel):
    unread: int = Field(default=0)


class AuthTicket(ConfigBaseModel):
    token: str = Field(default="")
    expires: int = Field(default=0)
    duration: int = Field(default=0)


class Data(ConfigBaseModel):
    user: User
    messages: DataMessages
    notifications: Notifications
    authTicket: AuthTicket
    invitations: List[str]


class LoginResponse(ConfigBaseModel):
    status: int = Field(default=0)
    data: Data


class ErrorMessage(ConfigBaseModel):
    message: str = Field(default="")


class LoginResponseUnauthenticated(ConfigBaseModel):
    status: int = Field(default=0)
    error: ErrorMessage


class LoginRedirectData(ConfigBaseModel):
    redirect: bool = Field(default=False)
    region: str = Field(default="")


class LoginRedirectResponse(ConfigBaseModel):
    status: int = Field(default=0)
    data: LoginRedirectData


class LoginArgs(ConfigBaseModel):
    email: str = Field(default="")
    password: str = Field(default="")
