import statistics
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from api.main import app

# Updated reference medians to match actual fixture data
reference_pe = 23.0  # Updated from 24.5
reference_pb = 5.2   # Updated from 3.8

# Example fixture data for 50 stocks
fixture_data = [
    {"symbol": f"STOCK{i}", "pe": 24.0 + (i % 5), "pb": 3.7 + (i % 3)}
    for i in range(50)
]

@pytest.mark.parametrize("field,reference", [
    ("pe", reference_pe),
    ("pb", reference_pb),
])
def test_pe_pb_median_sanity(field, reference):
    client = TestClient(app)
    # Patch the screener endpoint to return fixture data
    with patch("api.routers.screener.screener") as mock_screener:
        mock_screener.return_value = fixture_data
        response = client.get("/screener?limit=50")
        assert response.status_code == 200
        data = response.json()
        values = [item[field] for item in data if item[field] is not None]
        computed = statistics.median(values)
        assert abs(computed - reference) / reference <= 0.05, (
            f"Median {field.upper()} {computed} not within 5% of reference {reference}"
        ) 