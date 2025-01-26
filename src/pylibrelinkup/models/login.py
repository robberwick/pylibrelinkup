from typing import List

from pydantic import BaseModel, Field, field_validator

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
    policyAccept: int = Field(default=0)
    touAccept: int = Field(default=0)


class HistoryItem(BaseModel):
    policyAccept: int = Field(default=0)
    declined: bool | None = None


class RealWorldEvidence(BaseModel):
    policyAccept: int = Field(default=0)
    declined: bool = False
    touAccept: int = Field(default=0)
    history: List[HistoryItem] = []


class Consents(BaseModel):
    llu: Llu = Llu()
    realWorldEvidence: RealWorldEvidence = RealWorldEvidence()


class SystemMessages(BaseModel):
    firstUsePhoenix: int = Field(default=0)
    firstUsePhoenixReportsDataMerged: int = Field(default=0)
    lluGettingStartedBanner: int = Field(default=0)
    lluNewFeatureModal: int = Field(default=0)
    lluOnboarding: int = Field(default=0)
    lvWebPostRelease: str = Field(default="")


class System(BaseModel):
    messages: SystemMessages


class User(BaseModel):
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


class Notifications(BaseModel):
    unresolved: int = Field(default=0)


class DataMessages(BaseModel):
    unread: int = Field(default=0)


class AuthTicket(BaseModel):
    token: str = Field(default="")
    expires: int = Field(default=0)
    duration: int = Field(default=0)


class Data(BaseModel):
    user: User
    messages: DataMessages
    notifications: Notifications
    authTicket: AuthTicket
    invitations: List[str]

    @field_validator("invitations", mode="before")
    def coerce_null_to_empty_list(cls, v):
        return v if v is not None else []


class LoginResponse(BaseModel):
    status: int = Field(default=0)
    data: Data


class ErrorMessage(BaseModel):
    message: str = Field(default="")


class LoginResponseUnauthenticated(BaseModel):
    status: int = Field(default=0)
    error: ErrorMessage


class LoginRedirectData(BaseModel):
    redirect: bool = Field(default=False)
    region: str = Field(default="")


class LoginRedirectResponse(BaseModel):
    status: int = Field(default=0)
    data: LoginRedirectData


class LoginArgs(BaseModel):
    email: str = Field(default="")
    password: str = Field(default="")
