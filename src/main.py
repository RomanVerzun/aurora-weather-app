#!/usr/bin/env python3
"""
Консольное приложение для получения погоды через wttr.in
"""

import argparse
import sys
from weather_app import cli, cache


def main():
    """Главная функция приложения"""
    
    # Создаем парсер аргументов
    parser = argparse.ArgumentParser(
        description="Консольний додаток для отримання погоди",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Приклади використання:
  ./weather                      # Погода за автовизначенням IP
  ./weather --city Kyiv          # Погода для Києва
  ./weather --city "New York"    # Погода для міста з пробілом
  ./weather --watch              # Автооновлення кожні 5 хвилин
  ./weather --watch 60           # Автооновлення кожну хвилину
  ./weather --no-cache           # Без використання кешу
  ./weather --ttl 600            # Встановити TTL кешу 10 хвилин
        """
    )

    # Додаємо аргументи
    parser.add_argument(
        '--city', '-c',
        type=str,
        help='Назва міста (якщо не вказано - автовизначення за IP)'
    )
    
    parser.add_argument(
        '--watch', '-w',
        nargs='?',
        const=300,
        type=int,
        metavar='SECONDS',
        help='Режим автооновлення з інтервалом у секундах (за замовчуванням 300)'
    )
    
    parser.add_argument(
        '--no-cache',
        action='store_true',
        help='Не використовувати кеш'
    )
    
    parser.add_argument(
        '--ttl',
        type=int,
        default=cache.DEFAULT_TTL,
        help=f'TTL кешу в секундах (за замовчуванням {cache.DEFAULT_TTL})'
    )
    
    parser.add_argument(
        '--version', '-v',
        action='version',
        version='./weather 1.0.0'
    )

    # Парсимо аргументи
    args = parser.parse_args()

    # Визначаємо режим роботи
    use_cache = not args.no_cache

    # Якщо вказано режим watch
    if args.watch is not None:
        # В режимі watch, якщо місто не вказано - запитуємо у користувача
        city = args.city
        if city is None:
            city = cli.get_user_choice()
        
        cli.watch_mode(
            city=city,
            interval=args.watch,
            use_cache=use_cache,
            ttl=args.ttl
        )
    else:
        # Звичайний режим - одноразовий вивід
        city = args.city

        # Якщо місто не вказано - пропонуємо вибір
        if city is None:
            city = cli.get_user_choice()
        
        success = cli.fetch_and_display_weather(
            city=city,
            use_cache=use_cache,
            ttl=args.ttl
        )
        
        if not success:
            sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Вихід")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Критична помилка: {str(e)}", file=sys.stderr)
        sys.exit(1)
