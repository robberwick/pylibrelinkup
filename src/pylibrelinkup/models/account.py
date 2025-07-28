from typing import Optional

from pydantic import BaseModel, Field

__all__ = [
    "RegistrationArgs",
    "RegistrationResponse",
    "PasswordResetArgs",
    "PasswordResetResponse",
    "ResendVerificationArgs",
    "ResendVerificationResponse",
    "DeleteAccountArgs",
    "DeleteAccountResponse",
    "AcceptTermsArgs",
    "AcceptTermsResponse",
    "SignOutArgs",
    "SignOutResponse",
    "DismissMessageArgs",
    "DismissMessageResponse",
    "DismissAlarmArgs",
    "DismissAlarmResponse",
]


class RegistrationArgs(BaseModel):
    """Arguments for account registration."""
    email: str = Field(description="Email address for the account")
    password: str = Field(description="Password for the account")
    firstName: str = Field(description="First name")
    lastName: str = Field(description="Last name")
    country: str = Field(description="Country code")
    dateOfBirth: int = Field(description="Date of birth as timestamp")
    termsAccepted: bool = Field(description="Whether terms of use are accepted")
    privacyPolicyAccepted: bool = Field(description="Whether privacy policy is accepted")
    marketingEmails: bool = Field(default=False, description="Whether to receive marketing emails")
    realWorldEvidence: bool = Field(default=False, description="Whether to participate in real-world evidence")


class RegistrationResponse(BaseModel):
    """Response from account registration."""
    status: int = Field(description="Response status code")
    data: dict = Field(description="Registration response data")


class PasswordResetArgs(BaseModel):
    """Arguments for password reset request."""
    email: str = Field(description="Email address for password reset")


class PasswordResetResponse(BaseModel):
    """Response from password reset request."""
    status: int = Field(description="Response status code")
    data: dict = Field(description="Password reset response data")


class ResendVerificationArgs(BaseModel):
    """Arguments for resending email verification."""
    email: str = Field(description="Email address to resend verification to")


class ResendVerificationResponse(BaseModel):
    """Response from resend verification request."""
    status: int = Field(description="Response status code")
    data: dict = Field(description="Resend verification response data")


class DeleteAccountArgs(BaseModel):
    """Arguments for account deletion."""
    password: str = Field(description="Current password for verification")


class DeleteAccountResponse(BaseModel):
    """Response from account deletion request."""
    status: int = Field(description="Response status code")
    data: dict = Field(description="Delete account response data")


class AcceptTermsArgs(BaseModel):
    """Arguments for accepting terms of use or privacy policy."""
    type: str = Field(description="Type of acceptance: 'tou' for terms of use, 'pp' for privacy policy")
    accepted: bool = Field(description="Whether the terms are accepted")


class AcceptTermsResponse(BaseModel):
    """Response from accepting terms."""
    status: int = Field(description="Response status code")
    data: dict = Field(description="Accept terms response data")


class SignOutArgs(BaseModel):
    """Arguments for signing out."""
    pass


class SignOutResponse(BaseModel):
    """Response from sign out request."""
    status: int = Field(description="Response status code")
    data: dict = Field(description="Sign out response data")


class DismissMessageArgs(BaseModel):
    """Arguments for dismissing system messages."""
    messageId: str = Field(description="ID of the message to dismiss")


class DismissMessageResponse(BaseModel):
    """Response from dismissing a message."""
    status: int = Field(description="Response status code")
    data: dict = Field(description="Dismiss message response data")


class DismissAlarmArgs(BaseModel):
    """Arguments for dismissing alarms."""
    alarmId: str = Field(description="ID of the alarm to dismiss")


class DismissAlarmResponse(BaseModel):
    """Response from dismissing an alarm."""
    status: int = Field(description="Response status code")
    data: dict = Field(description="Dismiss alarm response data") 