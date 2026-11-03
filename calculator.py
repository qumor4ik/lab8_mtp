"""Модуль калькулятора, разработанный по методологии TDD (Средняя 4, 7)."""

from dataclasses import dataclass
import logging
import math
from typing import Any

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class CalculationRecord:
    """Неизменяемая запись об одной выполненной операции калькулятора."""

    operation: str
    operands: tuple[float, ...]
    result: float


def validate_number(value: Any, field_name: str) -> float:
    """Проверяет, что аргумент является конечным числом (исключая bool)."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        logger.error(
            "Ошибка типа параметра '%s': получено %r",
            field_name,
            value,
        )
        raise TypeError(f"Параметр '{field_name}' должен быть числом")

    numeric = float(value)
    if math.isnan(numeric) or math.isinf(numeric):
        logger.error(
            "Недопустимое значение параметра '%s': %s",
            field_name,
            numeric,
        )
        raise ValueError(
            f"Параметр '{field_name}' должен быть конечным числом"
        )
    return numeric


class Calculator:
    """Калькулятор с поддержкой базовых операций, истории и логирования."""

    def __init__(self) -> None:
        self._history: list[CalculationRecord] = []

    @property
    def history(self) -> list[CalculationRecord]:
        """Возвращает защищённую копию истории вычислений."""
        return list(self._history)

    def clear_history(self) -> None:
        """Очищает историю вычислений калькулятора."""
        self._history.clear()
        logger.info("История вычислений калькулятора очищена")

    def add(self, a: float | int, b: float | int) -> float:
        """Складывает два числа."""
        x = validate_number(a, "a")
        y = validate_number(b, "b")
        result = x + y
        self._record("add", (x, y), result)
        return result

    def subtract(self, a: float | int, b: float | int) -> float:
        """Вычитает второе число из первого."""
        x = validate_number(a, "a")
        y = validate_number(b, "b")
        result = x - y
        self._record("subtract", (x, y), result)
        return result

    def multiply(self, a: float | int, b: float | int) -> float:
        """Умножает два числа."""
        x = validate_number(a, "a")
        y = validate_number(b, "b")
        result = x * y
        self._record("multiply", (x, y), result)
        return result

    def divide(self, a: float | int, b: float | int) -> float:
        """Делит первое число на второе с защитой от деления на ноль."""
        x = validate_number(a, "a")
        y = validate_number(b, "b")
        if y == 0.0:
            logger.error("Попытка деления на ноль: %s / %s", x, y)
            raise ZeroDivisionError("Деление на ноль невозможно")
        result = x / y
        self._record("divide", (x, y), result)
        return result

    def power(self, base: float | int, exponent: float | int) -> float:
        """Возводит число base в степень exponent."""
        x = validate_number(base, "base")
        y = validate_number(exponent, "exponent")
        if x < 0 and not y.is_integer():
            logger.error(
                "Возведение отрицательного числа %s в дробную степень %s",
                x,
                y,
            )
            raise ValueError(
                "Нельзя возводить отрицательного числа в дробную степень"
            )
        result = float(math.pow(x, y))
        self._record("power", (x, y), result)
        return result

    def sqrt(self, value: float | int) -> float:
        """Вычисляет квадратный корень из неотрицательного числа."""
        x = validate_number(value, "value")
        if x < 0:
            logger.error("Попытка извлечения корня из отрицательного: %s", x)
            raise ValueError("Подкоренное выражение не может быть отрицательным")
        result = math.sqrt(x)
        self._record("sqrt", (x,), result)
        return result

    def _record(
        self,
        operation: str,
        operands: tuple[float, ...],
        result: float,
    ) -> None:
        entry = CalculationRecord(
            operation=operation,
            operands=operands,
            result=result,
        )
        self._history.append(entry)
        logger.info(
            "Выполнена операция %s%s = %s",
            operation,
            operands,
            result,
        )
