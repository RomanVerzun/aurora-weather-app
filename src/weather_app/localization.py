"""
Модуль локалізації описів погоди EN → UA
"""

# Словник перекладу описів погоди з англійської на українську
WEATHER_TRANSLATIONS = {
    # Ясно
    "Clear": "Ясно",
    "Sunny": "Сонячно",
    
    # Хмарність
    "Partly cloudy": "Мінлива хмарність",
    "Cloudy": "Хмарно",
    "Overcast": "Похмуро",
    
    # Туман
    "Mist": "Туман",
    "Fog": "Густий туман",
    "Freezing fog": "Морозний туман",
    
    # Дощ
    "Patchy rain possible": "Можливий дощ",
    "Patchy light rain": "Місцями легкий дощ",
    "Light rain": "Легкий дощ",
    "Moderate rain": "Помірний дощ",
    "Heavy rain": "Сильний дощ",
    "Light rain shower": "Легкий дощ",
    "Moderate or heavy rain shower": "Помірний або сильний дощ",
    "Torrential rain shower": "Злива",
    "Patchy light drizzle": "Місцями легка мряка",
    "Light drizzle": "Легка мряка",
    "Freezing drizzle": "Морозна мряка",
    "Heavy freezing drizzle": "Сильна морозна мряка",
    
    # Сніг
    "Patchy snow possible": "Можливий сніг",
    "Patchy light snow": "Місцями легкий сніг",
    "Light snow": "Легкий сніг",
    "Moderate snow": "Помірний сніг",
    "Heavy snow": "Сильний сніг",
    "Blowing snow": "Хуртовина",
    "Blizzard": "Заметіль",
    "Light snow showers": "Легкий снігопад",
    "Moderate or heavy snow showers": "Помірний або сильний снігопад",
    
    # Дощ зі снігом
    "Patchy sleet possible": "Можливий мокрий сніг",
    "Light sleet": "Легкий мокрий сніг",
    "Moderate or heavy sleet": "Помірний або сильний мокрий сніг",
    "Light sleet showers": "Легкий мокрий сніг",
    "Moderate or heavy sleet showers": "Помірний або сильний мокрий сніг",
    
    # Град
    "Ice pellets": "Крижана крупа",
    "Light showers of ice pellets": "Легка крижана крупа",
    "Moderate or heavy showers of ice pellets": "Помірна або сильна крижана крупа",
    
    # Гроза
    "Patchy light rain with thunder": "Місцями легкий дощ з грозою",
    "Moderate or heavy rain with thunder": "Помірний або сильний дощ з грозою",
    "Patchy light snow with thunder": "Місцями легкий сніг з грозою",
    "Moderate or heavy snow with thunder": "Помірний або сильний сніг з грозою",
    "Thundery outbreaks possible": "Можливі грози",
}

# Емодзі для погодних умов
WEATHER_EMOJI = {
    "clear": "☀️",
    "sunny": "☀️",
    "partly": "⛅",
    "cloudy": "☁️",
    "overcast": "☁️",
    "mist": "🌫️",
    "fog": "🌫️",
    "rain": "🌧️",
    "drizzle": "🌦️",
    "snow": "❄️",
    "blizzard": "🌨️",
    "sleet": "🌨️",
    "thunder": "⛈️",
    "shower": "🌦️",
}


def translate(description: str) -> str:
    """
    Перекладає опис погоди з англійської на українську

    Args:
        description: Опис погоди англійською

    Returns:
        Перекладений опис або оригінал, якщо переклад не знайдено
    """
    # Шукаємо точний збіг
    if description in WEATHER_TRANSLATIONS:
        return WEATHER_TRANSLATIONS[description]
    
    # Якщо точного збігу немає - повертаємо оригінал
    return description


def get_weather_emoji(description: str) -> str:
    """
    Повертає емодзі для опису погоди

    Args:
        description: Опис погоди

    Returns:
        Емодзі або значення за замовчуванням
    """
    description_lower = description.lower()
    
    # Шукаємо ключові слова в описі
    for keyword, emoji in WEATHER_EMOJI.items():
        if keyword in description_lower:
            return emoji
    
    # Якщо нічого не знайдено - повертаємо значення за замовчуванням
    return "🌡️"
