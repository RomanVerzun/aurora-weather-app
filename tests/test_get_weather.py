import pytest
from unittest import mock
import requests
import json
from src.weather_app.api import (
    get_weather,
    NetworkError,
    CityNotFoundError,
    InvalidResponseError,
)

@pytest.fixture
def mock_response():
    """Mock response object"""
    response = mock.Mock()
    response.status_code = 200
    response.json.return_value = {
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
    return response


def test_get_weather_with_city_success(mock_response):
    with mock.patch('requests.get', return_value=mock_response):
        result = get_weather("Kyiv")
        assert result == mock_response.json.return_value


def test_get_weather_without_city_success(mock_response):
    with mock.patch('requests.get', return_value=mock_response) as mock_get:
        result = get_weather()
        mock_get.assert_called_once_with("https://wttr.in/?format=j1", timeout=10)
        assert result == mock_response.json.return_value


def test_get_weather_with_city_url():
    with mock.patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "current_condition": [{"temp_C": "20", "weatherDesc": [{"value": "Clear"}]}],
            "nearest_area": [{"areaName": [{"value": "London"}]}]
        }
        get_weather("London")
        mock_get.assert_called_once_with("https://wttr.in/London?format=j1", timeout=10)


def test_get_weather_404_error():
    with mock.patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 404
        with pytest.raises(CityNotFoundError, match="Місто 'InvalidCity' не розпізнано"):
            get_weather("InvalidCity")


def test_get_weather_http_error():
    with mock.patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 500
        with pytest.raises(NetworkError, match="HTTP код відповіді: 500"):
            get_weather("City")


def test_get_weather_timeout_error():
    with mock.patch('requests.get', side_effect=requests.exceptions.Timeout):
        with pytest.raises(NetworkError, match="Таймаут при з'єднанні з сервером"):
            get_weather("City")


def test_get_weather_connection_error():
    with mock.patch('requests.get', side_effect=requests.exceptions.ConnectionError):
        with pytest.raises(NetworkError, match="Помилка з'єднання з сервером"):
            get_weather("City")


def test_get_weather_request_exception():
    with mock.patch('requests.get', side_effect=requests.exceptions.RequestException("Network issue")):
        with pytest.raises(NetworkError, match="Проблеми з мережею: Network issue"):
            get_weather("City")


def test_get_weather_json_decode_error():
    with mock.patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)
        with pytest.raises(InvalidResponseError, match="Некоректна відповідь сервера \\(не JSON\\)"):
            get_weather("City")


def test_get_weather_invalid_response_data():
    with mock.patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "nearest_area": [{"areaName": [{"value": "City"}]}],
            "invalid": "data"
        }
        with mock.patch('src.weather_app.api.validate_weather_data', return_value=False):
            with pytest.raises(InvalidResponseError, match="Відсутні обов'язкові поля у відповіді"):
                get_weather("City")


def test_get_weather_no_nearest_area():
    with mock.patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "current_condition": [{"temp_C": "20", "weatherDesc": [{"value": "Clear"}]}],
            "nearest_area": []
        }
        with pytest.raises(CityNotFoundError, match="Місто 'TestCity' не розпізнано"):
            get_weather("TestCity")


def test_get_weather_none_nearest_area():
    with mock.patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "current_condition": [{"temp_C": "20", "weatherDesc": [{"value": "Clear"}]}],
            "nearest_area": None
        }
        with pytest.raises(CityNotFoundError, match="Місто 'TestCity' не розпізнано"):
            get_weather("TestCity")