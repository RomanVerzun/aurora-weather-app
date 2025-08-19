"""
Модуль кешування даних про погоду з TTL
"""

import json
import os
import time
from typing import Dict, Optional
from pathlib import Path


CACHE_FILE = ".cache/weather.json"
DEFAULT_TTL = 300  # 5 хвилин за замовчуванням


def ensure_cache_dir():
    """Створює директорію для кешу, якщо її немає"""
    cache_dir = Path(CACHE_FILE).parent
    cache_dir.mkdir(parents=True, exist_ok=True)


def get_cache_key(city: Optional[str]) -> str:
    """
    Формує ключ для кешу

    Args:
        city: Назва міста або None для автовизначення

    Returns:
        Ключ для кешу
    """
    if city:
        return city.lower().strip()
    return "AUTO"


def get_from_cache(city: Optional[str], ttl: int = DEFAULT_TTL) -> Optional[Dict]:
    """
    Отримує дані з кешу, якщо вони актуальні

    Args:
        city: Назва міста або None для автовизначення
        ttl: Час життя кешу в секундах

    Returns:
        Дані з кешу або None, якщо кеш застарів/відсутній
    """
    ensure_cache_dir()

    # Перевіряємо існування файлу
    if not os.path.exists(CACHE_FILE):
        return None

    try:
        # Читаємо кеш
        with open(CACHE_FILE, 'r', encoding='utf-8') as f:
            cache_data = json.load(f)

        # Отримуємо ключ
        key = get_cache_key(city)

        # Перевіряємо наявність даних для ключа
        if key not in cache_data:
            return None

        cached_item = cache_data[key]

        # Перевіряємо TTL
        cached_at = cached_item.get("cached_at", 0)
        if time.time() - cached_at > ttl:
            return None

        return cached_item.get("data")

    except (json.JSONDecodeError, IOError, KeyError):
        # При будь-яких помилках читання кешу - ігноруємо його
        return None


def set_to_cache(city: Optional[str], data: Dict):
    """
    Зберігає дані в кеш

    Args:
        city: Назва міста або None для автовизначення
        data: Дані для збереження
    """
    ensure_cache_dir()

    # Читаємо існуючий кеш або створюємо новий
    cache_data = {}
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
        except (json.JSONDecodeError, IOError):
            # При помилці читання - створюємо новий кеш
            cache_data = {}

    # Додаємо/оновлюємо дані
    key = get_cache_key(city)
    cache_data[key] = {
        "data": data,
        "cached_at": time.time()
    }

    # Атомарний запис через тимчасовий файл
    temp_file = f"{CACHE_FILE}.tmp"
    try:
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, ensure_ascii=False, indent=2)

        # Перейменовуємо тимчасовий файл в основний
        os.replace(temp_file, CACHE_FILE)

    except IOError as e:
        # При помилці запису - видаляємо тимчасовий файл, якщо він існує
        if os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except:
                pass
        # Помилку запису ігноруємо - кеш не критичний для роботи


def clear_cache():
    """Повністю очищає кеш"""
    if os.path.exists(CACHE_FILE):
        try:
            os.remove(CACHE_FILE)
        except IOError:
            pass
