"""
Tests for /api/application/submit and /api/application/status endpoints
"""
import pytest
import requests
from datetime import date, timedelta


class TestApplicationStatus:
    """Tests for GET /api/application/status"""

    def test_status_requires_auth(self, api_base_url):
        """Should reject unauthenticated request"""
        response = requests.get(f"{api_base_url}/api/application/status")

        assert response.status_code == 401
        assert "error" in response.json()

    def test_get_status_with_invalid_token(self, api_base_url):
        """Should reject invalid session token"""
        response = requests.get(
            f"{api_base_url}/api/application/status",
            headers={"Authorization": "Bearer invalid-token"}
        )

        assert response.status_code == 401

    def test_get_status_no_application(self, api_base_url, auth_headers):
        """Should return has_application=False for new user"""
        response = requests.get(
            f"{api_base_url}/api/application/status",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["has_application"] is False

    def test_get_status_after_submission(self, api_base_url, auth_headers, valid_application_data):
        """Should return application details after submission"""
        # Submit application
        requests.post(
            f"{api_base_url}/api/application/submit",
            headers=auth_headers,
            json=valid_application_data
        )

        # Check status
        response = requests.get(
            f"{api_base_url}/api/application/status",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["has_application"] is True
        assert "application" in data
        assert data["application"]["full_name"] == valid_application_data["full_name"]


class TestApplicationSubmit:
    """Tests for POST /api/application/submit"""

    def test_submit_requires_auth(self, api_base_url, valid_application_data):
        """Should reject unauthenticated submission"""
        response = requests.post(
            f"{api_base_url}/api/application/submit",
            json=valid_application_data
        )

        assert response.status_code == 401

    @pytest.mark.smoke
    def test_submit_valid_application(self, api_base_url, auth_headers, valid_application_data):
        """Should successfully submit valid application"""
        response = requests.post(
            f"{api_base_url}/api/application/submit",
            headers=auth_headers,
            json=valid_application_data
        )

        assert response.status_code == 201
        data = response.json()
        assert data["message"] == "Application submitted successfully"
        assert "application" in data
        assert data["application"]["status"] in ["approved", "pending", "rejected"]

    def test_submit_duplicate_application(self, api_base_url, auth_headers, valid_application_data):
        """Should reject duplicate application submission"""
        # First submission
        requests.post(
            f"{api_base_url}/api/application/submit",
            headers=auth_headers,
            json=valid_application_data
        )

        # Second submission should fail
        response = requests.post(
            f"{api_base_url}/api/application/submit",
            headers=auth_headers,
            json=valid_application_data
        )

        assert response.status_code == 400
        assert "error" in response.json()


class TestApplicationValidation:
    """Tests for application field validations"""

    def test_full_name_required(self, api_base_url, auth_headers, valid_application_data):
        """Should reject empty full name"""
        data = valid_application_data.copy()
        data["full_name"] = ""

        response = requests.post(
            f"{api_base_url}/api/application/submit",
            headers=auth_headers,
            json=data
        )

        assert response.status_code == 400
        assert "full_name" in response.json().get("errors", {})

    def test_full_name_minimum_length(self, api_base_url, auth_headers, valid_application_data):
        """Should reject full name shorter than 2 characters"""
        data = valid_application_data.copy()
        data["full_name"] = "A"

        response = requests.post(
            f"{api_base_url}/api/application/submit",
            headers=auth_headers,
            json=data
        )

        assert response.status_code == 400
        assert "full_name" in response.json().get("errors", {})

    def test_national_id_required(self, api_base_url, auth_headers, valid_application_data):
        """Should reject empty national ID"""
        data = valid_application_data.copy()
        data["national_id"] = ""

        response = requests.post(
            f"{api_base_url}/api/application/submit",
            headers=auth_headers,
            json=data
        )

        assert response.status_code == 400
        assert "national_id" in response.json().get("errors", {})

    def test_national_id_minimum_length(self, api_base_url, auth_headers, valid_application_data):
        """Should reject national ID shorter than 5 characters"""
        data = valid_application_data.copy()
        data["national_id"] = "1234"

        response = requests.post(
            f"{api_base_url}/api/application/submit",
            headers=auth_headers,
            json=data
        )

        assert response.status_code == 400
        assert "national_id" in response.json().get("errors", {})

    def test_date_of_birth_invalid_format(self, api_base_url, auth_headers, valid_application_data):
        """Should reject invalid date format"""
        data = valid_application_data.copy()
        data["date_of_birth"] = "15-05-1990"

        response = requests.post(
            f"{api_base_url}/api/application/submit",
            headers=auth_headers,
            json=data
        )

        assert response.status_code == 400
        assert "date_of_birth" in response.json().get("errors", {})

    def test_date_of_birth_underage(self, api_base_url, auth_headers, valid_application_data):
        """Should reject applicant under 18 years old"""
        data = valid_application_data.copy()
        # Set DOB to 17 years ago
        underage_dob = date.today() - timedelta(days=17*365)
        data["date_of_birth"] = underage_dob.strftime("%Y-%m-%d")

        response = requests.post(
            f"{api_base_url}/api/application/submit",
            headers=auth_headers,
            json=data
        )

        assert response.status_code == 400
        assert "date_of_birth" in response.json().get("errors", {})

    def test_email_optional(self, api_base_url, auth_headers, valid_application_data):
        """Should accept submission without email"""
        data = valid_application_data.copy()
        data["email"] = ""

        response = requests.post(
            f"{api_base_url}/api/application/submit",
            headers=auth_headers,
            json=data
        )

        assert response.status_code == 201

    def test_email_invalid_format(self, api_base_url, auth_headers, valid_application_data):
        """Should reject invalid email format"""
        data = valid_application_data.copy()
        data["email"] = "not-an-email"

        response = requests.post(
            f"{api_base_url}/api/application/submit",
            headers=auth_headers,
            json=data
        )

        assert response.status_code == 400
        assert "email" in response.json().get("errors", {})

    def test_loan_amount_required(self, api_base_url, auth_headers, valid_application_data):
        """Should reject missing loan amount"""
        data = valid_application_data.copy()
        del data["loan_amount"]

        response = requests.post(
            f"{api_base_url}/api/application/submit",
            headers=auth_headers,
            json=data
        )

        assert response.status_code == 400
        assert "loan_amount" in response.json().get("errors", {})

    def test_loan_amount_below_minimum(self, api_base_url, auth_headers, valid_application_data):
        """Should reject loan amount below minimum (1000)"""
        data = valid_application_data.copy()
        data["loan_amount"] = 500

        response = requests.post(
            f"{api_base_url}/api/application/submit",
            headers=auth_headers,
            json=data
        )

        assert response.status_code == 400
        assert "loan_amount" in response.json().get("errors", {})

    def test_loan_amount_above_maximum(self, api_base_url, auth_headers, valid_application_data):
        """Should reject loan amount above maximum (5000000)"""
        data = valid_application_data.copy()
        data["loan_amount"] = 6000000

        response = requests.post(
            f"{api_base_url}/api/application/submit",
            headers=auth_headers,
            json=data
        )

        assert response.status_code == 400
        assert "loan_amount" in response.json().get("errors", {})

    def test_loan_amount_zero(self, api_base_url, auth_headers, valid_application_data):
        """Should reject zero loan amount"""
        data = valid_application_data.copy()
        data["loan_amount"] = 0

        response = requests.post(
            f"{api_base_url}/api/application/submit",
            headers=auth_headers,
            json=data
        )

        assert response.status_code == 400

    def test_loan_amount_negative(self, api_base_url, auth_headers, valid_application_data):
        """Should reject negative loan amount"""
        data = valid_application_data.copy()
        data["loan_amount"] = -1000

        response = requests.post(
            f"{api_base_url}/api/application/submit",
            headers=auth_headers,
            json=data
        )

        assert response.status_code == 400

    def test_loan_term_invalid(self, api_base_url, auth_headers, valid_application_data):
        """Should reject invalid loan term"""
        data = valid_application_data.copy()
        data["loan_term"] = 25  # Not in [15, 30, 45, 60]

        response = requests.post(
            f"{api_base_url}/api/application/submit",
            headers=auth_headers,
            json=data
        )

        assert response.status_code == 400
        assert "loan_term" in response.json().get("errors", {})

    @pytest.mark.parametrize("term", [15, 30, 45, 60])
    def test_loan_term_valid_options(self, api_base_url, auth_headers, valid_application_data, term):
        """Should accept valid loan term"""
        data = valid_application_data.copy()
        data["loan_term"] = term

        response = requests.post(
            f"{api_base_url}/api/application/submit",
            headers=auth_headers,
            json=data
        )

        assert response.status_code == 201

    def test_purpose_required(self, api_base_url, auth_headers, valid_application_data):
        """Should reject empty purpose"""
        data = valid_application_data.copy()
        data["purpose"] = ""

        response = requests.post(
            f"{api_base_url}/api/application/submit",
            headers=auth_headers,
            json=data
        )

        assert response.status_code == 400
        assert "purpose" in response.json().get("errors", {})


class TestLoanDecisionLogic:
    """Tests for loan decision outcomes"""

    def test_small_loan_approved(self, api_base_url, auth_headers, valid_application_data):
        """Small loan (<50000) for adult (25-59) should be approved"""
        data = valid_application_data.copy()
        data["loan_amount"] = 40000
        data["date_of_birth"] = "1990-01-01"  # ~35 years old

        response = requests.post(
            f"{api_base_url}/api/application/submit",
            headers=auth_headers,
            json=data
        )

        assert response.status_code == 201
        assert response.json()["application"]["status"] == "approved"

    def test_high_loan_pending(self, api_base_url, auth_headers, valid_application_data):
        """High loan (>=1000000) should be pending"""
        data = valid_application_data.copy()
        data["loan_amount"] = 1500000

        response = requests.post(
            f"{api_base_url}/api/application/submit",
            headers=auth_headers,
            json=data
        )

        assert response.status_code == 201
        assert response.json()["application"]["status"] == "pending"

    def test_senior_applicant_pending(self, api_base_url, auth_headers, valid_application_data):
        """Senior applicant (>=60 years) should be pending"""
        data = valid_application_data.copy()
        data["date_of_birth"] = "1960-01-01"  # ~65 years old

        response = requests.post(
            f"{api_base_url}/api/application/submit",
            headers=auth_headers,
            json=data
        )

        assert response.status_code == 201
        assert response.json()["application"]["status"] == "pending"

    def test_boundary_loan_amount_at_minimum(self, api_base_url, auth_headers, valid_application_data):
        """Loan at minimum boundary (1000) should be accepted"""
        data = valid_application_data.copy()
        data["loan_amount"] = 1000

        response = requests.post(
            f"{api_base_url}/api/application/submit",
            headers=auth_headers,
            json=data
        )

        assert response.status_code == 201

    def test_boundary_loan_amount_at_maximum(self, api_base_url, auth_headers, valid_application_data):
        """Loan at maximum boundary (5000000) should be accepted"""
        data = valid_application_data.copy()
        data["loan_amount"] = 5000000

        response = requests.post(
            f"{api_base_url}/api/application/submit",
            headers=auth_headers,
            json=data
        )

        assert response.status_code == 201
