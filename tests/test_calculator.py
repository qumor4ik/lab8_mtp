"""Модульные тесты pytest для калькулятора по методологии TDD (Средняя 4)."""

import logging
import pytest

from calculator import Calculator, validate_number


class TestValidateNumber:
    """Проверка функции строгой валидации числовых аргументов."""

    def test_valid_int_and_float(self) -> None:
        """Целые и вещественные числа успешно проходят проверку."""
        assert validate_number(10, "x") == 10.0
        assert validate_number(-3.5, "x") == -3.5
        assert validate_number(0, "x") == 0.0

    @pytest.mark.parametrize(
        "invalid_val",
        [True, False, "10", None, [1, 2]],
    )
    def test_rejects_non_numeric_and_bool(self, invalid_val: object) -> None:
        """Тип bool и нечисловые объекты вызывают исключение TypeError."""
        with pytest.raises(TypeError):
            validate_number(invalid_val, "arg")

    @pytest.mark.parametrize(
        "special_float",
        [float("nan"), float("inf"), float("-inf")],
    )
    def test_rejects_nan_and_infinity(self, special_float: float) -> None:
        """Значения NaN и бесконечность вызывают исключение ValueError."""
        with pytest.raises(ValueError):
            validate_number(special_float, "arg")


class TestCalculatorTDD:
    """Набор тестов TDD для проверки всех операций класса Calculator."""

    @pytest.fixture()
    def calc(self) -> Calculator:
        """Фикстура pytest, возвращающая новый экземпляр калькулятора."""
        return Calculator()

    @pytest.mark.parametrize(
        ("a", "b", "expected"),
        [
            (2, 3, 5.0),
            (-10, 4, -6.0),
            (0, 0, 0.0),
            (1.25, 2.75, 4.0),
        ],
    )
    def test_add(
        self, calc: Calculator, a: float, b: float, expected: float
    ) -> None:
        """Проверка операции сложения."""
        assert calc.add(a, b) == pytest.approx(expected)

    @pytest.mark.parametrize(
        ("a", "b", "expected"),
        [
            (10, 4, 6.0),
            (-5, -5, 0.0),
            (3.5, 1.2, 2.3),
        ],
    )
    def test_subtract(
        self, calc: Calculator, a: float, b: float, expected: float
    ) -> None:
        """Проверка операции вычитания."""
        assert calc.subtract(a, b) == pytest.approx(expected)

    @pytest.mark.parametrize(
        ("a", "b", "expected"),
        [
            (6, 7, 42.0),
            (-3, 5, -15.0),
            (123.45, 0, 0.0),
        ],
    )
    def test_multiply(
        self, calc: Calculator, a: float, b: float, expected: float
    ) -> None:
        """Проверка операции умножения."""
        assert calc.multiply(a, b) == pytest.approx(expected)

    def test_divide_valid(self, calc: Calculator) -> None:
        """Проверка корректного деления двух чисел."""
        assert calc.divide(15, 3) == pytest.approx(5.0)
        assert calc.divide(7, 2) == pytest.approx(3.5)

    def test_divide_by_zero_raises_error_and_logs(
        self,
        calc: Calculator,
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        """Деление на ноль выбрасывает ZeroDivisionError и пишет ERROR в лог."""
        with caplog.at_level(logging.ERROR):
            with pytest.raises(ZeroDivisionError, match="Деление на ноль"):
                calc.divide(10, 0)
        assert "Попытка деления на ноль" in caplog.text

    def test_power_and_negative_root_error(self, calc: Calculator) -> None:
        """Возведение в степень и запрет корня из отрицательного числа."""
        assert calc.power(2, 10) == pytest.approx(1024.0)
        assert calc.power(9, 0.5) == pytest.approx(3.0)
        with pytest.raises(ValueError, match="отрицательное число"):
            calc.power(-4, 0.5)

    def test_sqrt_valid_and_negative(self, calc: Calculator) -> None:
        """Извлечение квадратного корня и обработка отрицательного числа."""
        assert calc.sqrt(0) == pytest.approx(0.0)
        assert calc.sqrt(49) == pytest.approx(7.0)
        with pytest.raises(ValueError, match="не может быть отрицательным"):
            calc.sqrt(-1)

    def test_history_tracking_and_clear(self, calc: Calculator) -> None:
        """Проверка записи операций в историю и её очистки."""
        calc.add(5, 5)
        calc.multiply(3, 4)
        history = calc.history
        assert len(history) == 2
        assert history[0].operation == "add"
        assert history[0].result == 10.0
        assert history[1].operation == "multiply"
        assert history[1].result == 12.0

        calc.clear_history()
        assert calc.history == []
