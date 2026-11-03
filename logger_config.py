"""Модуль настройки системы логирования приложения (Средняя 7)."""

import logging
import sys

LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logging(
    level: int = logging.INFO,
    log_file: str | None = None,
) -> logging.Logger:
    """Настраивает корневой логгер и возвращает логгер приложения."""
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    formatter = logging.Formatter(fmt=LOG_FORMAT, datefmt=DATE_FORMAT)

    has_stream = any(
        isinstance(h, logging.StreamHandler)
        and not isinstance(h, logging.FileHandler)
        for h in root_logger.handlers
    )
    if not has_stream:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)

    if log_file is not None:
        if not isinstance(log_file, str) or not log_file.strip():
            raise ValueError("Путь к файлу логов должен быть непустой строкой")
        file_handler = logging.FileHandler(
            log_file.strip(),
            encoding="utf-8",
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)

    app_logger = logging.getLogger("lab8_app")
    app_logger.setLevel(level)
    app_logger.info("Система логирования инициализирована (level=%s)", level)
    return app_logger
