# Shared fixtures for all tests

import pytest
import random


#Base URLs
BASE_URL = "http://localhost:5173"
API_BASE_URL = "http://localhost:5001"


# Test credentials
VALID_OTP = "0000"
VALID_PHONE = "+254719000000"


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


@pytest.fixture(scope="session")
def api_base_url():
    return API_BASE_URL


@pytest.fixture
def valid_otp():
    return VALID_OTP


@pytest.fixture
def valid_phone():
    return VALID_PHONE


@pytest.fixture
def valid_personal_details():
    return {
        "full_name": "John Doe",
        "national_id": "CM12345678",
        "email": "john.doe@example.com",
        "date_of_birth": "1990-05-15"
    }


@pytest.fixture
def valid_loan_details():
    return {
        "loan_amount": 50000,
        "loan_term": 30,
        "purpose": "Business expansion"
    }


@pytest.fixture
def test_phone():
    """Generate unique phone number for each test"""
    unique_digits = ''.join(random.choices('0123456789', k=6))
    return f"+25470{unique_digits}"