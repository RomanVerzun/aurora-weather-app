"""
API клієнт для роботи з wttr.in
"""

import requests
from typing import Dict, Optional
import json


class NetworkError(Exception):
    """Помилка мережі при зверненні до API"""
    pass


class CityNotFoundError(Exception):
    """Місто не знайдено або не розпізнано"""
    pass


class InvalidResponseError(Exception):
    """Некоректна відповідь від сервера"""
    pass



def get_weather(city: Optional[str] = None) -> Dict:
    """
    Отримує дані про погоду для вказаного міста або за IP

    Args:
        city: Назва міста. Якщо None — автовизначення за IP

    Returns:
        Словник з даними про погоду

    Raises:
        NetworkError: При проблемах з мережею
        CityNotFoundError: Якщо місто не знайдено
        InvalidResponseError: При некоректній відповіді від сервера
    """
    # Формуємо URL
    if city:
        url = f"https://wttr.in/{city}?format=j1"
    else:
        url = "https://wttr.in/?format=j1"
    
    try:
        # Робимо запит
        response = requests.get(url, timeout=10)

        # Перевіряємо статус
        if response.status_code != 200:
            if response.status_code == 404:
                raise CityNotFoundError(f"Місто '{city}' не розпізнано")
            else:
                raise NetworkError(f"HTTP код відповіді: {response.status_code}")

        # Парсимо JSON
        data = response.json()

        # Спочатку перевіряємо, чи є nearest_area і чи місто розпізнано
        nearest_area = data.get("nearest_area")
        if not nearest_area or (
            isinstance(nearest_area, list) and len(nearest_area) == 0
        ):
            raise CityNotFoundError(f"Місто '{city}' не розпізнано")

        # Валідуємо обов'язкові поля
        if not validate_weather_data(data):
            raise InvalidResponseError("Відсутні обов'язкові поля у відповіді")
            
        return data
        
    except requests.exceptions.Timeout:
        raise NetworkError("Таймаут при з'єднанні з сервером")
    except requests.exceptions.ConnectionError:
        raise NetworkError("Помилка з'єднання з сервером")
    except requests.exceptions.RequestException as e:
        raise NetworkError(f"Проблеми з мережею: {str(e)}")
    except json.JSONDecodeError:
        raise InvalidResponseError("Некоректна відповідь сервера (не JSON)")


def validate_weather_data(data: Dict) -> bool:
    """
    Перевіряє наявність обов'язкових полів у відповіді API

    Args:
        data: Дані від API

    Returns:
        True якщо всі обов'язкові поля присутні
    """
    try:
        # Перевіряємо, що data є словником
        if not isinstance(data, dict):
            return False
            
        # Перевіряємо наявність основних полів
        current_condition = data.get("current_condition")
        nearest_area = data.get("nearest_area")
        
        # Перевіряємо, що current_condition є списком і не пустий
        if not isinstance(current_condition, list) or not current_condition:
            return False
            
        # Перевіряємо, що nearest_area є списком і не пустий  
        if not isinstance(nearest_area, list) or not nearest_area:
            return False
            
        current = current_condition[0]
        area = nearest_area[0]
        
        # Перевіряємо, що current і area є словниками
        if not isinstance(current, dict) or not isinstance(area, dict):
            return False

        # Перевіряємо температуру
        temp = current.get("temp_C")
        if temp is None:
            return False

        # Перевіряємо опис погоди
        weather_desc_list = current.get("weatherDesc")
        if not isinstance(weather_desc_list, list) or not weather_desc_list:
            return False
            
        weather_desc = weather_desc_list[0].get("value") if isinstance(weather_desc_list[0], dict) else None
        if not weather_desc:
            return False

        # Перевіряємо назву міста
        area_name_list = area.get("areaName")
        if not isinstance(area_name_list, list) or not area_name_list:
            return False
            
        area_name = area_name_list[0].get("value") if isinstance(area_name_list[0], dict) else None
        if not area_name:
            return False
            
        return True
        
    except (KeyError, IndexError, TypeError, AttributeError):
        return False


def extract_weather_info(data: Dict) -> Dict:
    """
    Витягує потрібну інформацію з відповіді API

    Args:
        data: Повні дані від API

    Returns:
        Словник з потрібними полями
    """
    current = data["current_condition"][0]
    area = data["nearest_area"][0]
    
    return {
        "city": area["areaName"][0]["value"],
        "country": area.get("country", [{}])[0].get("value", ""),
        "temperature": int(current["temp_C"]),
        "feels_like": int(current["FeelsLikeC"]),
        "description": current["weatherDesc"][0]["value"],
        "humidity": int(current["humidity"]),
        "wind_speed": int(current["windspeedKmph"]),
        "pressure": int(current["pressure"]),
    }
