"""
CLI інтерфейс для виведення погоди в консоль
"""

import os
import sys
import time
from typing import Dict, Optional
from . import api, cache, localization


def clear_screen():
    """Очищає екран консолі"""
    os.system('cls' if os.name == 'nt' else 'clear')


def format_weather_output(weather_info: Dict) -> str:
    """
    Форматує дані про погоду для виведення в консоль

    Args:
        weather_info: Словник з інформацією про погоду

    Returns:
        Відформатований рядок для виведення
    """
    # Перекладаємо опис
    description = weather_info["description"]
    translated_description = localization.translate(description)

    # Отримуємо емодзі
    emoji = localization.get_weather_emoji(description)

    # Форматуємо вивід
    output = []
    output.append("=" * 50)
    output.append(f"📍 Місто: {weather_info['city']}")
    if weather_info.get('country'):
        output[-1] += f", {weather_info['country']}"

    output.append(f"🌡️  Температура: {weather_info['temperature']}°C")
    output.append(f"🤔 Відчувається як: {weather_info['feels_like']}°C")
    output.append(f"{emoji} Опис: {translated_description}")
    output.append(f"💧 Вологість: {weather_info['humidity']}%")
    output.append(f"💨 Швидкість вітру: {weather_info['wind_speed']} км/год")
    output.append(f"⬇️  Тиск: {weather_info['pressure']} мбар")
    output.append("=" * 50)

    return "\n".join(output)


def print_error(message: str, exit_code: int = 1):
    """
    Виводить повідомлення про помилку та завершує програму

    Args:
        message: Повідомлення про помилку
        exit_code: Код виходу
    """
    print(f"❌ Помилка: {message}", file=sys.stderr)
    sys.exit(exit_code)


def get_user_choice() -> Optional[str]:
    """
    Інтерактивний вибір: ввести місто або використати автовизначення

    Returns:
        Назва міста або None для автовизначення
    """
    print("🌍 Оберіть спосіб визначення міста:")
    print("1. Ввести назву міста")
    print("2. Автоматичне визначення за IP")
    print("0. Вихід")

    while True:
        choice = input("\nВаш вибір (1/2/0): ").strip()

        if choice == "0":
            print("👋 Вихід")
            sys.exit(0)
        elif choice == "1":
            city = input("Введіть назву міста: ").strip()
            if city:
                return city
            else:
                print("❌ Назва міста не може бути порожньою")
        elif choice == "2":
            return None
        else:
            print("❌ Невірний вибір. Спробуйте ще раз.")

def fetch_and_display_weather(
    city: Optional[str] = None,
    use_cache: bool = True,
    ttl: int = cache.DEFAULT_TTL,
    quiet: bool = False
) -> bool:
    """
    Отримує та виводить дані про погоду

    Args:
        city: Назва міста або None для автовизначення
        use_cache: Чи використовувати кеш
        ttl: TTL кешу в секундах
        quiet: Тихий режим (не виводити повідомлення про кеш)

    Returns:
        True якщо дані успішно отримано та виведено
    """
    weather_data = None
    from_cache = False

    # Пробуємо отримати з кешу
    if use_cache:
        weather_data = cache.get_from_cache(city, ttl)
        if weather_data:
            from_cache = True
            if not quiet:
                print("📦 (дані з кешу)")

    # Якщо в кеші немає — запитуємо з API
    if not weather_data:
        try:
            if not quiet:
                print("🔄 Завантаження даних...")
            weather_data = api.get_weather(city)

            # Зберігаємо в кеш
            if use_cache:
                cache.set_to_cache(city, weather_data)

        except api.CityNotFoundError as e:
            print_error(str(e), exit_code=2)
            return False
        except api.NetworkError as e:
            print_error(str(e), exit_code=7)
            return False
        except api.InvalidResponseError as e:
            print_error(str(e), exit_code=3)
            return False
        except Exception as e:
            print_error(f"Невідома помилка: {str(e)}", exit_code=1)
            return False

    # Витягуємо потрібну інформацію
    try:
        weather_info = api.extract_weather_info(weather_data)
    except (KeyError, ValueError) as e:
        print_error("Некоректна структура даних від API", exit_code=3)
        return False

    # Виводимо результат
    print(format_weather_output(weather_info))

    return True


def watch_mode(
    city: Optional[str] = None,
    interval: int = 300,
    use_cache: bool = True,
    ttl: int = cache.DEFAULT_TTL
):
    """
    Режим автоматичного оновлення погоди

    Args:
        city: Назва міста або None для автовизначення
        interval: Інтервал оновлення в секундах
        use_cache: Чи використовувати кеш
        ttl: TTL кешу в секундах
    """
    print(f"🔄 Режим автооновлення кожні {interval} секунд")
    print("Натисніть Ctrl+C для виходу\n")

    try:
        while True:
            # Очищаємо екран
            clear_screen()

            # Показуємо час оновлення
            current_time = time.strftime("%H:%M:%S")
            print(f"⏰ Оновлено: {current_time}\n")

            # Отримуємо та відображаємо погоду
            fetch_and_display_weather(city, use_cache, ttl, quiet=True)

            # Показуємо таймер до наступного оновлення
            print(f"\n⏳ Наступне оновлення через {interval} секунд...")

            # Чекаємо
            time.sleep(interval)

    except KeyboardInterrupt:
        print("\n\n👋 Вихід з режиму автооновлення")
        sys.exit(0)
