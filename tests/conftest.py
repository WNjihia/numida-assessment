# Shared fixtures for all tests

import pytest


#Base URLs
BASE_URL = "http://localhost:5173"
API_BASE_URL = "http://localhost:5001"


# Test credentials
VALID_OTP = "0000"


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


@pytest.fixture(scope="session")
def api_base_url():
    return API_BASE_URL


@pytest.fixture
def valid_otp():
    return VALID_OTP