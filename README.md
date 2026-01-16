#  Cервис для управления базой данных видеофайлов.

## Технологии
- FastAPI
- PostgreSQL
- SQLAlchemy 2.0
- Pydantic 2.0
- Docker Compose

## Запуск проекта

### 1. Клонирование репозитория
```bash
git clone https://github.com/murlinmurlo/video-db-api.git
cd video-db-api

### 2. Сборка
```bash
docker compose up --build 

## API Endpoints
POST /videos - Добавить новое видео
GET /videos - Получить список видео (с фильтрацией)
GET /videos/{id} - Получить видео по ID
PATCH /videos/{id}/status - Обновить статус видео

## Документация API
После запуска доступна по адресу:
Swagger UI: http://localhost:8000/docs