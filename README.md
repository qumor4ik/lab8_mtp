\# Лабораторная работа №8: Экосистемы Python, их использование



\*\*Выполнил:\*\* Нестеров Вадим Сергеевич  

\*\*Группа:\*\* 221141  

\*\*Вариант:\*\* 2



\## Описание заданий (Вариант 2)



В проекте реализованы все пять заданий варианта 2 с соблюдением стандартов PEP 8 и методологии TDD:



\- \*\*Средняя 2 (Добавить зависимость `requests`):\*\* Зависимость `requests` зафиксирована в `pyproject.toml` (Poetry) и `requirements.txt`. В модуле `http\_client.py` реализован класс `ApiServiceClient` с поддержкой `requests.Session`, таймаутов и валидации ответов.

\- \*\*Средняя 4 (Реализовать TDD для калькулятора):\*\* По методологии Test-Driven Development сначала разработан набор тестов `tests/test\_calculator.py` на базе `pytest` (параметризованные тесты, граничные случаи, проверка исключений `ZeroDivisionError`, `TypeError`, `ValueError`), после чего реализован модуль `calculator.py`.

\- \*\*Средняя 7 (Использовать `logging`):\*\* В модуле `logger\_config.py` настроено структурированное логирование с форматированием времени, уровня и источника сообщений. Все операции калькулятора и HTTP-клиента логируются и проверяются через фикстуру `caplog` в `pytest`.

\- \*\*Повышенная 2 (Настроить CI GitHub Actions с `pytest`):\*\* В файле `.github/workflows/ci.yml` настроен пайплайн непрерывной интеграции на события `push` и `pull\_request` с кэшированием `pip`, проверкой стиля `flake8` и запуском тестов `pytest -v`.

\- \*\*Повышенная 6 (Настроить Docker для приложения):\*\* Создан `Dockerfile` на базе `python:3.12-slim` с запуском от непривилегированного пользователя `appuser` и файлом `.dockerignore`.



\## Структура проекта



\- `calculator.py` — класс `Calculator` и функции строгой валидации чисел (Средняя 4).

\- `http\_client.py` — HTTP-клиент `ApiServiceClient` на базе `requests` (Средняя 2).

\- `logger\_config.py` — конфигурация системы логирования `logging` (Средняя 7).

\- `tests/test\_calculator.py` — модульные тесты `pytest` для калькулятора (TDD, Средняя 4).

\- `tests/test\_http\_and\_logging.py` — модульные тесты `pytest` для `requests` и `logging`.

\- `main.py` — точка входа с поддержкой CLI-параметров (`--test`, `--url`).

\- `pyproject.toml` — конфигурация проекта для менеджера пакетов `Poetry` и `pytest`.

\- `requirements.txt` и `requirements-dev.txt` — списки runtime и dev-зависимостей.

\- `.github/workflows/ci.yml` — конфигурация CI GitHub Actions (Повышенная 2).

\- `Dockerfile` и `.dockerignore` — контейнеризация приложения (Повышенная 6).

\- `.flake8` и `.gitignore` — конфигурация линтера и правила игнорирования Git.



\## Установка и запуск



\### 1. Установка зависимостей (через pip или Poetry)



Через `pip`:

```bash

pip install -r requirements-dev.txt

```



Через `Poetry`:

```bash

poetry install

```



\### 2. Запуск модульных тестов `pytest` и линтера `flake8`



```bash

pytest -v

flake8 .

```



Либо через точку входа:

```bash

python main.py --test

```



\### 3. Запуск демонстрационного режима приложения



```bash

python main.py

```



\### 4. Сборка и запуск в Docker (Повышенная 6)



Сборка образа:

```bash

docker build -t lab8-mtp:v1.0 .

```



Запуск контейнера (демонстрация):

```bash

docker run --rm lab8-mtp:v1.0

```



Запуск тестов `pytest` внутри Docker-контейнера:

```bash

docker run --rm lab8-mtp:v1.0 pytest -v

```



\## Пример вывода в консоли



```text

2026-11-03 14:00:00 | INFO     | lab8\_app | Система логирования инициализирована (level=20)

2026-11-03 14:00:00 | INFO     | lab8\_app | === Лабораторная работа №8 (Вариант 2) ===

2026-11-03 14:00:00 | INFO     | lab8\_app | Выполнил: Нестеров Вадим Сергеевич, группа 221141

2026-11-03 14:00:00 | INFO     | calculator | Выполнена операция add(25.0, 17.0) = 42.0

2026-11-03 14:00:00 | INFO     | calculator | Выполнена операция multiply(42.0, 2.0) = 84.0

2026-11-03 14:00:00 | INFO     | calculator | Выполнена операция sqrt(144.0,) = 12.0

2026-11-03 14:00:00 | INFO     | lab8\_app | \[Средняя 4: TDD Калькулятор] 25 + 17 = 42.0; \* 2 = 84.0; sqrt(144) = 12.0

2026-11-03 14:00:00 | INFO     | lab8\_app | \[Средняя 7: Logging] Записей в истории калькулятора: 3

2026-11-03 14:00:00 | INFO     | http\_client | Отправка GET-запроса через requests: https://jsonplaceholder.typicode.com/todos/1

2026-11-03 14:00:00 | INFO     | http\_client | Успешный ответ от https://jsonplaceholder.typicode.com/todos/1 (HTTP 200)

2026-11-03 14:00:00 | INFO     | lab8\_app | \[Средняя 2: requests] Статус: 200 | Ключи ответа: \['userId', 'id', 'title', 'completed']

```

