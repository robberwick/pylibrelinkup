from typing import List

from pydantic import BaseModel

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


class Llu(BaseModel):
    policyAccept: int
    touAccept: int


class Consents(BaseModel):
    llu: Llu


class SystemMessages(BaseModel):
    firstUsePhoenix: int
    firstUsePhoenixReportsDataMerged: int
    lluGettingStartedBanner: int
    lluNewFeatureModal: int
    lluOnboarding: int
    lvWebPostRelease: str


class System(BaseModel):
    messages: SystemMessages


class User(BaseModel):
    id: str
    firstName: str
    lastName: str
    email: str
    country: str
    uiLanguage: str
    communicationLanguage: str
    accountType: str
    uom: str
    dateFormat: str
    timeFormat: str
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


class Notifications(BaseModel):
    unresolved: int


class DataMessages(BaseModel):
    unread: int


class AuthTicket(BaseModel):
    token: str
    expires: int
    duration: int


class Data(BaseModel):
    user: User
    messages: DataMessages
    notifications: Notifications
    authTicket: AuthTicket
    invitations: List[str]


class LoginResponse(BaseModel):
    status: int
    data: Data


class ErrorMessage(BaseModel):
    message: str


class LoginResponseUnauthenticated(BaseModel):
    status: int
    error: ErrorMessage


class LoginRedirectData(BaseModel):
    redirect: bool
    region: str


class LoginRedirectResponse(BaseModel):
    status: int
    data: LoginRedirectData


class LoginArgs(BaseModel):
    email: str = ""
    password: str = ""
