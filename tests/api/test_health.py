"""
Tests for /api/health and root endpoints
"""
import requests


class TestHealthCheck:
    """Tests for GET /api/health"""

    def test_health_check_returns_healthy(self, api_base_url):
        """Should return healthy status"""
        response = requests.get(f"{api_base_url}/api/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data

    def test_health_check_timestamp_format(self, api_base_url):
        """Should return valid ISO timestamp"""
        response = requests.get(f"{api_base_url}/api/health")

        data = response.json()
        timestamp = data["timestamp"]
        # Should be ISO format like "2024-01-15T10:30:00.000000"
        assert "T" in timestamp


class TestRootEndpoint:
    """Tests for GET /"""

    def test_root_returns_welcome_message(self, api_base_url):
        """Should return welcome message"""
        response = requests.get(f"{api_base_url}/")

        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "Loan Application" in data["message"]
