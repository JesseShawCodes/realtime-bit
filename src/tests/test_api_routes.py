
import pytest
import requests
import os

# Get the base URL from an environment variable or use a default
BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:8000")

def is_api_running():
    """Check if the API is running before starting tests."""
    try:
        response = requests.get(f"{BASE_URL}/health")
        return response.status_code == 200
    except requests.ConnectionError:
        return False

# Skip all tests in this module if the API is not running
pytestmark = pytest.mark.skipif(not is_api_running(), reason="API is not running")


def test_health_check():
    """Test the /health endpoint."""
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_get_history():
    """Test the /data/history endpoint."""
    response = requests.get(f"{BASE_URL}/data/history?limit=5")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 5
    if data:
        assert "asset" in data[0]
        assert "price" in data[0]
        assert "timestamp" in data[0]

def test_get_latest():
    """Test the /data/latest endpoint."""
    response = requests.get(f"{BASE_URL}/data/latest?limit=10")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 10
    if data:
        assert "asset" in data[0]
        assert "price" in data[0]
        assert "timestamp" in data[0]

def test_get_metrics():
    """Test the /data/metrics endpoint."""
    response = requests.get(f"{BASE_URL}/data/metrics")
    assert response.status_code == 200
    data = response.json()
    if "error" not in data:
        assert "min" in data
        assert "max" in data
        assert "avg" in data
        assert isinstance(data["min"], (int, float))
        assert isinstance(data["max"], (int, float))
        assert isinstance(data["avg"], (int, float))

def test_get_metrics_with_limit():
    """Test the /data/metrics endpoint with a limit."""
    response = requests.get(f"{BASE_URL}/data/metrics?limit=5")
    assert response.status_code == 200
    data = response.json()
    if "error" not in data:
        assert "min" in data
        assert "max" in data
        assert "avg" in data

