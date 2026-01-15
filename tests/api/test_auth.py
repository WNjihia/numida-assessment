"""
Tests for /api/auth/request-otp and /api/auth/verify-otp endpoints
"""
import pytest
import requests


class TestRequestOTP:
    """Tests for POST /api/auth/request-otp"""

    def test_request_otp_with_valid_phone(self, api_base_url, test_phone):
        """Should successfully request OTP for valid phone number"""
        response = requests.post(
            f"{api_base_url}/api/auth/request-otp",
            json={"phone_number": test_phone}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "OTP sent successfully"
        assert data["phone_number"] == test_phone

    def test_request_otp_with_invalid_phone_short(self, api_base_url):
        """Should reject phone number that is too short"""
        response = requests.post(
            f"{api_base_url}/api/auth/request-otp",
            json={"phone_number": "12345"}
        )

        assert response.status_code == 400
        assert "Invalid" in response.json()["error"]

    def test_request_otp_with_empty_phone(self, api_base_url):
        """Should reject empty phone number"""
        response = requests.post(
            f"{api_base_url}/api/auth/request-otp",
            json={"phone_number": ""}
        )

        assert response.status_code == 400
        assert "error" in response.json()

    def test_request_otp_with_missing_phone(self, api_base_url):
        """Should reject request without phone number"""
        response = requests.post(
            f"{api_base_url}/api/auth/request-otp",
            json={}
        )

        assert response.status_code == 400

    def test_request_otp_with_letters_in_phone(self, api_base_url):
        """Should reject phone number containing letters"""
        response = requests.post(
            f"{api_base_url}/api/auth/request-otp",
            json={"phone_number": "+256abc123456"}
        )

        assert response.status_code == 400

    def test_request_otp_accepts_various_formats(self, api_base_url):
        """Should accept phone numbers in various valid formats"""
        valid_formats = [
            "+256700000001",
            "256700000002",
            "0700000003",
            "+1 555 123 4567",
            "555-123-4567"
        ]

        for phone in valid_formats:
            response = requests.post(
                f"{api_base_url}/api/auth/request-otp",
                json={"phone_number": phone}
            )
            assert response.status_code == 200, f"Failed for phone: {phone}"


class TestVerifyOTP:
    """Tests for POST /api/auth/verify-otp"""

    @pytest.mark.smoke
    def test_verify_otp_with_valid_credentials(self, api_base_url, test_phone, valid_otp):
        """Should successfully verify OTP and return session token"""
        # First request OTP
        requests.post(
            f"{api_base_url}/api/auth/request-otp",
            json={"phone_number": test_phone}
        )

        # Then verify
        response = requests.post(
            f"{api_base_url}/api/auth/verify-otp",
            json={"phone_number": test_phone, "otp": valid_otp}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Authentication successful"
        assert "session_token" in data
        assert data["phone_number"] == test_phone

    def test_verify_otp_with_invalid_otp(self, api_base_url, test_phone):
        """Should reject invalid OTP"""
        # First request OTP
        requests.post(
            f"{api_base_url}/api/auth/request-otp",
            json={"phone_number": test_phone}
        )

        # Try invalid OTP
        response = requests.post(
            f"{api_base_url}/api/auth/verify-otp",
            json={"phone_number": test_phone, "otp": "9999"}
        )

        assert response.status_code == 401
        assert "error" in response.json()

    def test_verify_otp_without_requesting_first(self, api_base_url, test_phone):
        """Should reject OTP verification without prior OTP request"""
        response = requests.post(
            f"{api_base_url}/api/auth/verify-otp",
            json={"phone_number": test_phone, "otp": "0000"}
        )

        assert response.status_code == 401

    def test_verify_otp_with_missing_otp(self, api_base_url, test_phone):
        """Should reject empty OTP"""
        requests.post(
            f"{api_base_url}/api/auth/request-otp",
            json={"phone_number": test_phone}
        )

        response = requests.post(
            f"{api_base_url}/api/auth/verify-otp",
            json={"phone_number": test_phone, "otp": ""}
        )

        assert response.status_code == 401

    def test_verify_otp_with_invalid_phone(self, api_base_url):
        """Should reject invalid phone number format"""
        response = requests.post(
            f"{api_base_url}/api/auth/verify-otp",
            json={"phone_number": "invalid", "otp": "0000"}
        )

        assert response.status_code == 400

    def test_session_token_is_unique(self, api_base_url, valid_otp):
        """Should generate unique session tokens for each login"""
        tokens = []

        for i in range(3):
            phone = f"+25670000{i:04d}"
            requests.post(
                f"{api_base_url}/api/auth/request-otp",
                json={"phone_number": phone}
            )
            response = requests.post(
                f"{api_base_url}/api/auth/verify-otp",
                json={"phone_number": phone, "otp": valid_otp}
            )
            tokens.append(response.json()["session_token"])

        # All tokens should be unique
        assert len(tokens) == len(set(tokens))
