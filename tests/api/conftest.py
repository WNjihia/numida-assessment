"""
API Test Fixtures
"""
import pytest
import requests
import random


@pytest.fixture(scope="session")
def api_base_url():
    return "http://localhost:5001"


@pytest.fixture
def valid_otp():
    return "0000"


@pytest.fixture
def test_phone():
    """Generate unique phone number for each test"""
    unique_digits = ''.join(random.choices('0123456789', k=6))
    return f"+25670{unique_digits}"


@pytest.fixture
def authenticated_session(api_base_url, test_phone, valid_otp):
    """Create an authenticated session and return the token"""
    # Request OTP
    requests.post(
        f"{api_base_url}/api/auth/request-otp",
        json={"phone_number": test_phone}
    )

    # Verify OTP
    response = requests.post(
        f"{api_base_url}/api/auth/verify-otp",
        json={"phone_number": test_phone, "otp": valid_otp}
    )

    data = response.json()
    return {
        "token": data["session_token"],
        "phone_number": test_phone
    }


@pytest.fixture
def auth_headers(authenticated_session):
    """Return authorization headers for authenticated requests"""
    return {"Authorization": f"Bearer {authenticated_session['token']}"}


@pytest.fixture
def valid_application_data():
    """Valid application data for submission"""
    return {
        "full_name": "John Doe",
        "national_id": "CM12345678",
        "email": "john.doe@example.com",
        "date_of_birth": "1990-05-15",
        "loan_amount": 50000,
        "loan_term": 30,
        "purpose": "Business expansion"
    }
