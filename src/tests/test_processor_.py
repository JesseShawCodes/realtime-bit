
import pytest
from datetime import datetime, timezone
from app.data.processor import normalize, update_history, compute_metrics

def test_normalize():
    """
    Test the normalize function.
    """
    raw_data = {
        "bitcoin": {"usd": 50000},
        "ethereum": {"usd": 4000}
    }
    normalized = normalize(raw_data)
    assert len(normalized) == 2
    for item in normalized:
        assert "asset" in item
        assert "price" in item
        assert "timestamp" in item
        assert isinstance(item["price"], (int, float))
        assert isinstance(item["asset"], str)
        assert isinstance(item["timestamp"], str)

def test_normalize_empty():
    """
    Test normalize with empty input.
    """
    normalized = normalize(None)
    assert normalized == []
    normalized = normalize({})
    assert normalized == []

def test_update_history_and_compute_metrics():
    """
    Test update_history and compute_metrics.
    """
    # Clear history for a clean test
    from app.data.processor import _price_history
    _price_history.clear()

    normalized_data = [
        {"asset": "bitcoin", "price": 51000, "timestamp": datetime.now(timezone.utc).isoformat()},
        {"asset": "ethereum", "price": 4100, "timestamp": datetime.now(timezone.utc).isoformat()}
    ]
    update_history(normalized_data)

    metrics = compute_metrics()
    assert "bitcoin" in metrics
    assert "ethereum" in metrics
    assert metrics["bitcoin"]["min"] == 51000
    assert metrics["bitcoin"]["max"] == 51000
    assert metrics["bitcoin"]["moving_avg"] == 51000

    normalized_data_2 = [
        {"asset": "bitcoin", "price": 52000, "timestamp": datetime.now(timezone.utc).isoformat()},
    ]
    update_history(normalized_data_2)
    metrics = compute_metrics()
    assert metrics["bitcoin"]["min"] == 51000
    assert metrics["bitcoin"]["max"] == 52000
    assert metrics["bitcoin"]["moving_avg"] == 51500

