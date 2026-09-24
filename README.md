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
- [ ] Этап 2 — CI/CD пайплайн
- [ ] Этап 3 — Инструменты безопасности
- [ ] Этап 4 — Анализ