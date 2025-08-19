import pytest
from src.weather_app.api import extract_weather_info

def test_extract_weather_info_complete_data():
    """Test extraction with complete valid data"""
    data = {
        "current_condition": [{
            "temp_C": "25",
            "FeelsLikeC": "28",
            "weatherDesc": [{"value": "Sunny"}],
            "humidity": "60",
            "windspeedKmph": "10",
            "pressure": "1013"
        }],
        "nearest_area": [{
            "areaName": [{"value": "Kyiv"}],
            "country": [{"value": "Ukraine"}]
        }]
    }
    result = extract_weather_info(data)
    expected = {
        "city": "Kyiv",
        "country": "Ukraine",
        "temperature": 25,
        "feels_like": 28,
        "description": "Sunny",
        "humidity": 60,
        "wind_speed": 10,
        "pressure": 1013,
    }
    assert result == expected


def test_extract_weather_info_missing_country():
    """Test extraction when country is missing"""
    data = {
        "current_condition": [{
            "temp_C": "20",
            "FeelsLikeC": "22",
            "weatherDesc": [{"value": "Cloudy"}],
            "humidity": "70",
            "windspeedKmph": "15",
            "pressure": "1010"
        }],
        "nearest_area": [{
            "areaName": [{"value": "London"}]
        }]
    }
    result = extract_weather_info(data)
    assert result["city"] == "London"
    assert result["country"] == ""
    assert result["temperature"] == 20


def test_extract_weather_info_empty_country():
    """Test extraction when country is empty list"""
    data = {
        "current_condition": [{
            "temp_C": "15",
            "FeelsLikeC": "18",
            "weatherDesc": [{"value": "Rainy"}],
            "humidity": "85",
            "windspeedKmph": "20",
            "pressure": "1005"
        }],
        "nearest_area": [{
            "areaName": [{"value": "Paris"}],
            "country": []
        }]
    }
    result = extract_weather_info(data)
    assert result["city"] == "Paris"
    assert result["country"] == ""


def test_extract_weather_info_country_no_value():
    """Test extraction when country has no value"""
    data = {
        "current_condition": [{
            "temp_C": "30",
            "FeelsLikeC": "35",
            "weatherDesc": [{"value": "Hot"}],
            "humidity": "40",
            "windspeedKmph": "5",
            "pressure": "1020"
        }],
        "nearest_area": [{
            "areaName": [{"value": "Madrid"}],
            "country": [{}]
        }]
    }
    result = extract_weather_info(data)
    assert result["city"] == "Madrid"
    assert result["country"] == ""


def test_extract_weather_info_negative_temperature():
    """Test extraction with negative temperature"""
    data = {
        "current_condition": [{
            "temp_C": "-10",
            "FeelsLikeC": "-15",
            "weatherDesc": [{"value": "Snow"}],
            "humidity": "90",
            "windspeedKmph": "25",
            "pressure": "1000"
        }],
        "nearest_area": [{
            "areaName": [{"value": "Moscow"}],
            "country": [{"value": "Russia"}]
        }]
    }
    result = extract_weather_info(data)
    assert result["temperature"] == -10
    assert result["feels_like"] == -15
    assert result["description"] == "Snow"


def test_extract_weather_info_zero_values():
    """Test extraction with zero values"""
    data = {
        "current_condition": [{
            "temp_C": "0",
            "FeelsLikeC": "0",
            "weatherDesc": [{"value": "Freezing"}],
            "humidity": "0",
            "windspeedKmph": "0",
            "pressure": "1000"
        }],
        "nearest_area": [{
            "areaName": [{"value": "Arctic"}],
            "country": [{"value": "Norway"}]
        }]
    }
    result = extract_weather_info(data)
    assert result["temperature"] == 0
    assert result["feels_like"] == 0
    assert result["humidity"] == 0
    assert result["wind_speed"] == 0


def test_extract_weather_info_high_values():
    """Test extraction with high numeric values"""
    data = {
        "current_condition": [{
            "temp_C": "45",
            "FeelsLikeC": "50",
            "weatherDesc": [{"value": "Extremely Hot"}],
            "humidity": "100",
            "windspeedKmph": "120",
            "pressure": "1050"
        }],
        "nearest_area": [{
            "areaName": [{"value": "Desert City"}],
            "country": [{"value": "UAE"}]
        }]
    }
    result = extract_weather_info(data)
    assert result["temperature"] == 45
    assert result["feels_like"] == 50
    assert result["humidity"] == 100
    assert result["wind_speed"] == 120
    assert result["pressure"] == 1050