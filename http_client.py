"""Модуль HTTP-клиента на базе библиотеки requests (Средняя 2, Средняя 7)."""

from dataclasses import dataclass
import logging
from typing import Any

import requests

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class HttpResult:
    """Структурированный результат выполнения HTTP-запроса."""

    url: str
    status_code: int
    ok: bool
    payload: dict[str, Any]


def validate_url(url: Any) -> str:
    """Проверяет, что передан корректный HTTP/HTTPS URL."""
    if not isinstance(url, str):
        raise TypeError("URL должен быть строкой")
    cleaned = url.strip()
    if not cleaned.startswith(("http://", "https://")):
        raise ValueError("URL должен начинаться с http:// или https://")
    return cleaned


class ApiServiceClient:
    """Клиент для выполнения HTTP-запросов через библиотеку requests."""

    DEFAULT_TIMEOUT: float = 5.0

    def __init__(
        self,
        session: requests.Session | None = None,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        if isinstance(timeout, bool) or not isinstance(timeout, (int, float)):
            raise TypeError("Таймаут должен быть числом")
        if timeout <= 0:
            raise ValueError("Таймаут должен быть положительным числом")
        self.timeout = float(timeout)
        self._session = session or requests.Session()

    def fetch_json(self, url: str) -> HttpResult:
        """Выполняет GET-запрос через requests и возвращает JSON-данные."""
        valid_url = validate_url(url)
        logger.info("Отправка GET-запроса через requests: %s", valid_url)

        try:
            response = self._session.get(valid_url, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as exc:
            logger.warning(
                "Ошибка сети при запросе к %s: %s",
                valid_url,
                exc,
            )
            raise
        except ValueError as exc:
            logger.error("Некорректный JSON от ресурса %s", valid_url)
            raise ValueError("Ответ сервера не является валидным JSON") from exc

        if not isinstance(data, dict):
            data = {"items": data}

        result = HttpResult(
            url=valid_url,
            status_code=int(response.status_code),
            ok=bool(response.ok),
            payload=data,
        )
        logger.info(
            "Успешный ответ от %s (HTTP %d)",
            valid_url,
            result.status_code,
        )
        return result
