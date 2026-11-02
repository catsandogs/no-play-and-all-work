# DevSecOps Calculator API

API-калькулятор на FastAPI. Упакован в Docker-контейнер.

## Стек

- Python 3.12
- FastAPI
- Uvicorn
- Pydantic
- Docker

## Запуск локально

    pip install -r requirements.txt
    uvicorn main:app --reload

Swagger UI: http://localhost:8000/docs

## Запуск в Docker

    docker build -t calc-api:1.0.0 .
    docker run -d --name calc-container -p 8000:8000 calc-api:1.0.0

Swagger UI: http://localhost:8000/docs

## Команда

- Тренихин Михаил Александрович, РИ-431003
- Шамбатуева Анастасия Михайловна, РИ-431003

## Этапы

- [x] Этап 1 — API-калькулятор и Docker
- [x] Этап 2 — CI/CD пайплайн
- [x] Этап 3 — Инструменты безопасности
- [x] Этап 4 — Анализ

## Структура пайплайна (Jenkins)

Файл `Jenkinsfile` в корне репозитория. Триггер — `Poll SCM` (`* * * * *`), сборка запускается автоматически при каждом пуше в GitHub.

| # | Стадия | Инструмент | Что делает |
|---|--------|------------|------------|
| 1 | checkout | git | Скачивает актуальный код из репозитория. |
| 2 | semgrep | Semgrep (SAST) | Статический анализ исходного кода на уязвимости. |
| 3 | trivy fs | Trivy (SCA) | Сканирует `requirements.txt` на известные CVE. |
| 4 | docker build | Docker | Собирает образ `calculator-api:${BUILD_NUMBER}`. |
| 5 | trivy image | Trivy (Container Scan) | Сканирует собранный образ (ОС + библиотеки). |
| 6 | deploy | Docker | Останавливает старый контейнер, запускает новый, проверяет `/health`. |

## Результаты сканирования

### Semgrep (SAST)
    Ran 87 rules on 10 files: 0 findings.

Проверены файлы: `main.py`, `Dockerfile`, `templates/index.html`, `static/style.css`.
Уязвимостей не обнаружено. Код не содержит `eval()`, SQL-инъекций, хардкод-паролей, небезопасных `subprocess`.

### Trivy Image (Container Scan)
    calculator-api:latest (debian 13.7)
    Total: 45 (HIGH: 45, CRITICAL: 0)

    Python (python-pkg)
    Total: 3 (HIGH: 3, CRITICAL: 0)

**Найденные уязвимости:**

| Компонент | CVE | Severity | Описание | Fixed Version |
|-----------|-----|----------|----------|---------------|
| starlette 0.38.6 | CVE-2024-47874 | HIGH | DoS через `multipart/form-data` | 0.40.0 |
| starlette 0.38.6 | CVE-2026-48818 | HIGH | SSRF и кража NTLM-учётных данных через UNC-пути | 1.1.0 |
| starlette 0.38.6 | CVE-2026-54283 | HIGH | DoS через `application/x-www-form-urlencoded` | 1.3.1 |
| debian (системные пакеты) | — | HIGH | 45 уязвимостей в `util-linux`, `systemd`, `ncurses`, `sqlite`, `perl` | обновление базового образа |

## Анализ и рекомендации

**Semgrep** подтверждает: исходный код приложения безопасен. Разработчик не использует опасные функции и корректно работает с пользовательским вводом через Pydantic.

**Trivy** выявляет уязвимости в цепочке поставок (Supply Chain):
1. **Библиотека `starlette 0.38.6`** — подтягивается транзитивно через `fastapi 0.115.0`. Содержит 3 HIGH-уязвимости, включая критичную DoS (CVE-2024-47874).
2. **Базовый образ `python:3.12-slim` (Debian 13.7)** — содержит 45 HIGH-уязвимостей в системных пакетах, которые не видны при анализе исходников.

**Вывод:** безопасный код — не гарантия безопасности приложения. Уязвимости приходят из зависимостей и базового образа. Это подтверждает необходимость комплексного подхода DevSecOps: SAST (Semgrep) + SCA + Container Scan (Trivy).

**Рекомендации по устранению:**

1. Обновить `fastapi` до версии, использующей `starlette >= 0.40.0`:
       fastapi==0.115.4
       starlette==0.41.3

2. Перейти на более лёгкий базовый образ (`python:3.12-alpine` или `python:3.12-slim-bookworm` с регулярным обновлением), что сократит количество системных CVE.

3. Запускать контейнер от непривилегированного пользователя — добавить в `Dockerfile`:
       RUN useradd -m appuser
       USER appuser

4. Ограничить ресурсы контейнера при деплое (`--memory`, `--cpus`).

5. Настроить политику блокировки сборки при наличии CRITICAL-уязвимостей (флаг `--exit-code 1` в Trivy).
