"""Тесты pytest для HTTP-клиента requests (Средняя 2) и logging (Средняя 7)."""

import logging
from pathlib import Path
from unittest.mock import MagicMock

import pytest
import requests

from http_client import ApiServiceClient, validate_url
from logger_config import setup_logging


class TestHttpClientRequests:
    """Проверка работы ApiServiceClient с библиотекой requests."""

    def test_validate_url(self) -> None:
        """Проверка валидации корректных и некорректных URL."""
        test_url = "https://api.github.com"
        assert validate_url(f" {test_url} ") == test_url
        with pytest.raises(TypeError):
            validate_url(12345)
        with pytest.raises(ValueError):
            validate_url("ftp://example.com")

    def test_fetch_json_success(
        self,
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        """Проверка успешного получения JSON и записи в лог."""
        mock_session = MagicMock(spec=requests.Session)
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.ok = True
        mock_response.json.return_value = {"id": 1, "title": "Lab 8"}
        mock_session.get.return_value = mock_response

        client = ApiServiceClient(session=mock_session, timeout=3.0)
        test_url = "https://jsonplaceholder.typicode.com/todos/1"
        with caplog.at_level(logging.INFO):
            res = client.fetch_json(test_url)

        assert res.status_code == 200
        assert res.ok is True
        assert res.payload["title"] == "Lab 8"
        mock_session.get.assert_called_once_with(
            test_url,
            timeout=3.0,
        )
        assert "Успешный ответ от" in caplog.text

    def test_fetch_json_network_error(
        self,
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        """Проверка обработки исключений requests.RequestException."""
        mock_session = MagicMock(spec=requests.Session)
        mock_session.get.side_effect = requests.ConnectionError("Offline")

        client = ApiServiceClient(session=mock_session)
        with caplog.at_level(logging.WARNING):
            with pytest.raises(requests.RequestException):
                client.fetch_json("https://example.com/api")

        assert "Ошибка сети при запросе" in caplog.text

    def test_invalid_timeout_rejected(self) -> None:
        """Проверка отклонения некорректного таймаута в конструкторе."""
        with pytest.raises(TypeError):
            ApiServiceClient(timeout=True)
        with pytest.raises(ValueError):
            ApiServiceClient(timeout=-1.0)


class TestLoggingConfiguration:
    """Проверка настройки логирования (Средняя 7)."""

    def test_setup_logging_with_file(self, tmp_path: Path) -> None:
        """Проверка записи логов в файл и валидации пути."""
        log_file = tmp_path / "app_test.log"
        app_logger = setup_logging(
            level=logging.INFO,
            log_file=str(log_file),
        )
        app_logger.info("Тестовое сообщение для проверки файла логов")

        root_logger = logging.getLogger()
        for handler in list(root_logger.handlers):
            if isinstance(handler, logging.FileHandler):
                handler.flush()
                handler.close()
                root_logger.removeHandler(handler)

        content = log_file.read_text(encoding="utf-8")
        assert "Тестовое сообщение для проверки файла логов" in content

    def test_setup_logging_rejects_empty_file_path(self) -> None:
        """Пустая строка пути к лог-файлу вызывает ValueError."""
        with pytest.raises(ValueError):
            setup_logging(log_file="   ")
