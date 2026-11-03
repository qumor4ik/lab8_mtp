"""Точка входа для лабораторной работы №8 (Вариант 2)."""

import argparse
import logging
import sys

import pytest
import requests

from calculator import Calculator
from http_client import ApiServiceClient
from logger_config import setup_logging


def run_demo(api_url: str) -> None:
    """Демонстрирует работу всех компонентов лабораторной работы №8."""
    logger = setup_logging(level=logging.INFO)
    logger.info("=== Лабораторная работа №8 (Вариант 2) ===")
    logger.info("Выполнил: Нестеров Вадим Сергеевич, группа 221141")

    # Средняя 4 и Средняя 7: Калькулятор (TDD) + логирование
    calc = Calculator()
    sum_res = calc.add(25, 17)
    mul_res = calc.multiply(sum_res, 2)
    sqrt_res = calc.sqrt(144)
    logger.info(
        "[Средняя 4: TDD Калькулятор] 25 + 17 = %s; * 2 = %s; sqrt(144) = %s",
        sum_res,
        mul_res,
        sqrt_res,
    )
    logger.info(
        "[Средняя 7: Logging] Записей в истории калькулятора: %d",
        len(calc.history),
    )

    # Средняя 2: Зависимость requests
    client = ApiServiceClient(timeout=3.0)
    try:
        http_res = client.fetch_json(api_url)
        logger.info(
            "[Средняя 2: requests] Статус: %d | Ключи ответа: %s",
            http_res.status_code,
            list(http_res.payload.keys()),
        )
    except requests.RequestException as exc:
        logger.warning(
            "[Средняя 2: requests] Внешний ресурс недоступен (%s). "
            "Для автономной проверки используйте pytest.",
            exc,
        )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Разбирает аргументы командной строки."""
    parser = argparse.ArgumentParser(
        description="Лабораторная работа №8: Экосистемы Python (Вариант 2)",
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Запустить модульные тесты pytest",
    )
    parser.add_argument(
        "--url",
        type=str,
        default="https://jsonplaceholder.typicode.com/todos/1",
        help="URL для демонстрационного GET-запроса через requests",
    )
    return parser.parse_args(argv)


def main() -> int:
    """Главная функция маршрутизации режимов запуска."""
    args = parse_args()
    if args.test:
        return int(pytest.main(["-v"]))

    run_demo(api_url=args.url)
    return 0


if __name__ == "__main__":
    sys.exit(main())
