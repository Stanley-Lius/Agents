import pytest
from unittest.mock import patch, MagicMock

# Import the module to test
import map_search

# Test 1: Unit Test with Mocked Google Maps API
@patch("map_search.get_gmaps_client")
def test_search_nearby_restaurants_success(mock_get_client):
    # Setup mock
    mock_client = MagicMock()
    mock_client.places.return_value = {
        "results": [
            {"place_id": "123", "name": "Mock BBQ", "formatted_address": "123 Main St", "rating": 4.5, "price_level": 2}
        ]
    }
    mock_get_client.return_value = mock_client

    # Execute
    # We use a unique keyword to bypass the simple global cache for this test.
    results = map_search.search_nearby_restaurants(location="25.0, 121.0", keyword="MockBBQTest")

    # Assert
    assert len(results) == 1
    assert results[0]["name"] == "Mock BBQ"
    mock_client.places.assert_called_once()

@patch("map_search.get_gmaps_client")
def test_search_nearby_restaurants_empty(mock_get_client):
    mock_client = MagicMock()
    mock_client.places.return_value = {"results": []}
    mock_get_client.return_value = mock_client

    results = map_search.search_nearby_restaurants(location="25.0, 121.0", keyword="EmptyTest")

    assert len(results) == 0

@patch("map_search.get_gmaps_client")
def test_get_route_duration_success(mock_get_client):
    mock_client = MagicMock()
    mock_client.distance_matrix.return_value = {
        "status": "OK",
        "rows": [{"elements": [{"status": "OK", "distance": {"text": "5 km"}, "duration": {"text": "10 mins", "value": 600}}]}]
    }
    mock_get_client.return_value = mock_client

    result = map_search.get_route_duration(origin="A", destination="B")

    assert result is not None
    assert result["duration_text"] == "10 mins"
    assert result["duration_value_seconds"] == 600
