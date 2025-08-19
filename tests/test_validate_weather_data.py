import pytest
from src.weather_app.api import validate_weather_data

def test_validate_weather_data_valid_complete():
    """Test validation with complete valid data"""
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
    assert validate_weather_data(data) is True


def test_validate_weather_data_missing_temp_c():
    """Test validation when temp_C is missing"""
    data = {
        "current_condition": [{
            "weatherDesc": [{"value": "Sunny"}],
        }],
        "nearest_area": [{
            "areaName": [{"value": "Kyiv"}]
        }]
    }
    assert validate_weather_data(data) is False


def test_validate_weather_data_temp_c_none():
    """Test validation when temp_C is None"""
    data = {
        "current_condition": [{
            "temp_C": None,
            "weatherDesc": [{"value": "Sunny"}],
        }],
        "nearest_area": [{
            "areaName": [{"value": "Kyiv"}]
        }]
    }
    assert validate_weather_data(data) is False


def test_validate_weather_data_missing_weather_desc():
    """Test validation when weatherDesc is missing"""
    data = {
        "current_condition": [{
            "temp_C": "25",
        }],
        "nearest_area": [{
            "areaName": [{"value": "Kyiv"}]
        }]
    }
    assert validate_weather_data(data) is False


def test_validate_weather_data_empty_weather_desc():
    """Test validation when weatherDesc is empty"""
    data = {
        "current_condition": [{
            "temp_C": "25",
            "weatherDesc": []
        }],
        "nearest_area": [{
            "areaName": [{"value": "Kyiv"}]
        }]
    }
    assert validate_weather_data(data) is False


def test_validate_weather_data_weather_desc_no_value():
    """Test validation when weatherDesc has no value"""
    data = {
        "current_condition": [{
            "temp_C": "25",
            "weatherDesc": [{}]
        }],
        "nearest_area": [{
            "areaName": [{"value": "Kyiv"}]
        }]
    }
    assert validate_weather_data(data) is False


def test_validate_weather_data_missing_area_name():
    """Test validation when areaName is missing"""
    data = {
        "current_condition": [{
            "temp_C": "25",
            "weatherDesc": [{"value": "Sunny"}]
        }],
        "nearest_area": [{}]
    }
    assert validate_weather_data(data) is False


def test_validate_weather_data_empty_area_name():
    """Test validation when areaName is empty"""
    data = {
        "current_condition": [{
            "temp_C": "25",
            "weatherDesc": [{"value": "Sunny"}]
        }],
        "nearest_area": [{
            "areaName": []
        }]
    }
    assert validate_weather_data(data) is False


def test_validate_weather_data_area_name_no_value():
    """Test validation when areaName has no value"""
    data = {
        "current_condition": [{
            "temp_C": "25",
            "weatherDesc": [{"value": "Sunny"}]
        }],
        "nearest_area": [{
            "areaName": [{}]
        }]
    }
    assert validate_weather_data(data) is False


def test_validate_weather_data_missing_current_condition():
    """Test validation when current_condition is missing"""
    data = {
        "nearest_area": [{
            "areaName": [{"value": "Kyiv"}]
        }]
    }
    assert validate_weather_data(data) is False


def test_validate_weather_data_empty_current_condition():
    """Test validation when current_condition is empty"""
    data = {
        "current_condition": [],
        "nearest_area": [{
            "areaName": [{"value": "Kyiv"}]
        }]
    }
    assert validate_weather_data(data) is False


def test_validate_weather_data_missing_nearest_area():
    """Test validation when nearest_area is missing"""
    data = {
        "current_condition": [{
            "temp_C": "25",
            "weatherDesc": [{"value": "Sunny"}]
        }]
    }
    assert validate_weather_data(data) is False


def test_validate_weather_data_empty_nearest_area():
    """Test validation when nearest_area is empty"""
    data = {
        "current_condition": [{
            "temp_C": "25",
            "weatherDesc": [{"value": "Sunny"}]
        }],
        "nearest_area": []
    }
    assert validate_weather_data(data) is False


def test_validate_weather_data_invalid_structure():
    """Test validation with invalid data structure"""
    data = "invalid"
    assert validate_weather_data(data) is False


def test_validate_weather_data_none():
    """Test validation with None data"""
    assert validate_weather_data(None) is False


def test_validate_weather_data_empty_dict():
    """Test validation with empty dictionary"""
    assert validate_weather_data({}) is False