import pytest
from unittest.mock import Mock, patch
from requests import HTTPError

from pylibrelinkup import PyLibreLinkUp
from pylibrelinkup.models.account import (
    AcceptTermsArgs,
    DeleteAccountArgs,
    DismissAlarmArgs,
    DismissMessageArgs,
    PasswordResetArgs,
    RegistrationArgs,
    ResendVerificationArgs,
    SignOutArgs,
)
from pylibrelinkup.exceptions import (
    AccountDeletionError,
    AlarmDismissalError,
    EmailVerificationResendError,
    MessageDismissalError,
    PasswordResetError,
    RegistrationError,
    SignOutError,
    TermsAcceptanceError,
)


class TestAccountManagement:
    """Test account management functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.client = PyLibreLinkUp("test@example.com", "password")
        self.client.token = "test_token"
        self.client.account_id_hash = "test_hash"

    @patch("requests.post")
    def test_register_account_success(self, mock_post):
        """Test successful account registration."""
        mock_response = Mock()
        mock_response.json.return_value = {"status": 200, "data": {"message": "Account created"}}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        registration_args = RegistrationArgs(
            email="new@example.com",
            password="newpassword",
            firstName="John",
            lastName="Doe",
            country="US",
            dateOfBirth=1234567890,
            termsAccepted=True,
            privacyPolicyAccepted=True,
        )

        response = self.client.register_account(registration_args)
        assert response.status == 200
        assert response.data["message"] == "Account created"

    @patch("requests.post")
    def test_register_account_failure(self, mock_post):
        """Test account registration failure."""
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = HTTPError("Registration failed")
        mock_post.return_value = mock_response

        registration_args = RegistrationArgs(
            email="new@example.com",
            password="newpassword",
            firstName="John",
            lastName="Doe",
            country="US",
            dateOfBirth=1234567890,
            termsAccepted=True,
            privacyPolicyAccepted=True,
        )

        with pytest.raises(RegistrationError):
            self.client.register_account(registration_args)

    @patch("requests.post")
    def test_reset_password_success(self, mock_post):
        """Test successful password reset."""
        mock_response = Mock()
        mock_response.json.return_value = {"status": 200, "data": {"message": "Reset email sent"}}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        reset_args = PasswordResetArgs(email="test@example.com")
        response = self.client.reset_password(reset_args)
        assert response.status == 200
        assert response.data["message"] == "Reset email sent"

    @patch("requests.post")
    def test_reset_password_failure(self, mock_post):
        """Test password reset failure."""
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = HTTPError("Reset failed")
        mock_post.return_value = mock_response

        reset_args = PasswordResetArgs(email="test@example.com")
        with pytest.raises(PasswordResetError):
            self.client.reset_password(reset_args)

    @patch("requests.post")
    def test_resend_verification_email_success(self, mock_post):
        """Test successful email verification resend."""
        mock_response = Mock()
        mock_response.json.return_value = {"status": 200, "data": {"message": "Email sent"}}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        resend_args = ResendVerificationArgs(email="test@example.com")
        response = self.client.resend_verification_email(resend_args)
        assert response.status == 200
        assert response.data["message"] == "Email sent"

    @patch("requests.post")
    def test_resend_verification_email_failure(self, mock_post):
        """Test email verification resend failure."""
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = HTTPError("Resend failed")
        mock_post.return_value = mock_response

        resend_args = ResendVerificationArgs(email="test@example.com")
        with pytest.raises(EmailVerificationResendError):
            self.client.resend_verification_email(resend_args)

    @patch("requests.post")
    def test_delete_account_success(self, mock_post):
        """Test successful account deletion."""
        mock_response = Mock()
        mock_response.json.return_value = {"status": 200, "data": {"message": "Account deleted"}}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        delete_args = DeleteAccountArgs(password="current_password")
        response = self.client.delete_account(delete_args)
        assert response.status == 200
        assert response.data["message"] == "Account deleted"

    @patch("requests.post")
    def test_delete_account_failure(self, mock_post):
        """Test account deletion failure."""
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = HTTPError("Deletion failed")
        mock_post.return_value = mock_response

        delete_args = DeleteAccountArgs(password="current_password")
        with pytest.raises(AccountDeletionError):
            self.client.delete_account(delete_args)

    @patch("requests.post")
    def test_accept_terms_success(self, mock_post):
        """Test successful terms acceptance."""
        mock_response = Mock()
        mock_response.json.return_value = {"status": 200, "data": {"message": "Terms accepted"}}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        accept_args = AcceptTermsArgs(type="tou", accepted=True)
        response = self.client.accept_terms(accept_args)
        assert response.status == 200
        assert response.data["message"] == "Terms accepted"

    @patch("requests.post")
    def test_accept_terms_failure(self, mock_post):
        """Test terms acceptance failure."""
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = HTTPError("Acceptance failed")
        mock_post.return_value = mock_response

        accept_args = AcceptTermsArgs(type="tou", accepted=True)
        with pytest.raises(TermsAcceptanceError):
            self.client.accept_terms(accept_args)

    @patch("requests.post")
    def test_sign_out_success(self, mock_post):
        """Test successful sign out."""
        mock_response = Mock()
        mock_response.json.return_value = {"status": 200, "data": {"message": "Signed out"}}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        sign_out_args = SignOutArgs()
        response = self.client.sign_out(sign_out_args)
        assert response.status == 200
        assert response.data["message"] == "Signed out"

    @patch("requests.post")
    def test_sign_out_failure(self, mock_post):
        """Test sign out failure."""
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = HTTPError("Sign out failed")
        mock_post.return_value = mock_response

        sign_out_args = SignOutArgs()
        with pytest.raises(SignOutError):
            self.client.sign_out(sign_out_args)

    @patch("requests.post")
    def test_dismiss_message_success(self, mock_post):
        """Test successful message dismissal."""
        mock_response = Mock()
        mock_response.json.return_value = {"status": 200, "data": {"message": "Message dismissed"}}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        dismiss_args = DismissMessageArgs(messageId="msg_123")
        response = self.client.dismiss_message(dismiss_args)
        assert response.status == 200
        assert response.data["message"] == "Message dismissed"

    @patch("requests.post")
    def test_dismiss_message_failure(self, mock_post):
        """Test message dismissal failure."""
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = HTTPError("Dismissal failed")
        mock_post.return_value = mock_response

        dismiss_args = DismissMessageArgs(messageId="msg_123")
        with pytest.raises(MessageDismissalError):
            self.client.dismiss_message(dismiss_args)

    @patch("requests.post")
    def test_dismiss_alarm_success(self, mock_post):
        """Test successful alarm dismissal."""
        mock_response = Mock()
        mock_response.json.return_value = {"status": 200, "data": {"message": "Alarm dismissed"}}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        dismiss_args = DismissAlarmArgs(alarmId="alarm_123")
        response = self.client.dismiss_alarm(dismiss_args)
        assert response.status == 200
        assert response.data["message"] == "Alarm dismissed"

    @patch("requests.post")
    def test_dismiss_alarm_failure(self, mock_post):
        """Test alarm dismissal failure."""
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = HTTPError("Dismissal failed")
        mock_post.return_value = mock_response

        dismiss_args = DismissAlarmArgs(alarmId="alarm_123")
        with pytest.raises(AlarmDismissalError):
            self.client.dismiss_alarm(dismiss_args)

    def test_authenticated_methods_require_token(self):
        """Test that authenticated methods require a token."""
        client = PyLibreLinkUp("test@example.com", "password")
        
        # These methods should raise an error when not authenticated
        with pytest.raises(Exception):
            client.delete_account(DeleteAccountArgs(password="test"))
        
        with pytest.raises(Exception):
            client.accept_terms(AcceptTermsArgs(type="tou", accepted=True))
        
        with pytest.raises(Exception):
            client.sign_out(SignOutArgs())
        
        with pytest.raises(Exception):
            client.dismiss_message(DismissMessageArgs(messageId="test"))
        
        with pytest.raises(Exception):
            client.dismiss_alarm(DismissAlarmArgs(alarmId="test")) 