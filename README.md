# DeviceStats

DeviceStats — это сервис для сбора, хранения и анализа данных, поступающих с устройств. Приложение реализовано на Python с использованием FastAPI для создания REST API, Celery для фоновых задач, PostgreSQL для хранения данных и Redis как брокера и backend для Celery. Проект полностью контейнеризирован с помощью Docker Compose.

[Посмотреть техническое задание](specification.md)


## Функциональность
- Сбор данных:
Принимает JSON с измерениями (x, y, z) от устройств по их идентификатору и сохраняет их в базу данных.
- Анализ данных:
Производится агрегация данных (минимум, максимум, сумма, медиана, количество) для каждого устройства за заданный период или за всё время.
- Фоновые задачи:
С помощью Celery реализована задача асинхронного пересчёта агрегированных данных для всех устройств.
- Нагрузочное тестирование:
Для проверки производительности используется Locust.

## Структура проекта
    DeviceStats/
    ├── app/
    │   ├── Dockerfile             # Dockerfile для сервиса приложения
    │   ├── celery_app.py          # Настройка Celery (создание объекта Celery и импорт задач)
    │   ├── crud.py                # CRUD-операции для работы с базой данных
    │   ├── database.py            # Конфигурация SQLAlchemy (engine, SessionLocal, get_db)
    │   ├── init_db.py             # Скрипт инициализации базы данных (для локального теста)
    │   ├── main.py                # FastAPI-приложение и маршруты
    │   ├── models.py              # ORM-модели SQLAlchemy
    │   ├── requirements.txt       # Зависимости для приложения
    │   ├── schemas.py             # Pydantic схемы для валидации данных
    │   └── tasks.py               # Определение фоновых задач для Celery
    ├── docker-compose.yml         # Конфигурация для Docker Compose (определяет сервисы: app, worker, db, redis)
    ├── .env                       # Переменные окружения (опционально)
    ├── Readme.md                  # Документация по проекту
    └── tests/
        ├── Dockerfile             # Dockerfile для тестового сервиса (Locust)
        ├── locustfile.py          # Сценарий нагрузочного тестирования с Locust
        └── requirements.txt       # Зависимости для тестов

## Установка и запуск

### Требования:
- Docker
- Docker-compose
- Python 3.8+
- PostgreSQL (если не используется Docker)
- Redis (если не используется Docker)
- Git

### Установка
1. Клонируйте репозиторий:
```bash
git clone https://your.git.repo/DeviceStats.git
cd DeviceStats
```
2. Настройка переменных окружения

В файле docker-compose.yml не забываем отредактировать:

    POSTGRES_USER:
    POSTGRES_PASSWORD: 
    POSTGRES_DB: 
    DB_HOST:
    DB_PORT:
    REDIS_HOST:
    REDIS_PORT:

В файле database.py не забываем отредактировать:

    DB_USER
    DB_PASSWORD
    DB_NAME
    DB_HOST
    DB_PORT

В файле celery_app.py:

    REDIS_HOST
    REDIS_PORT 

3. Запуск приложения (из корня проекта)
```bash
docker-compose up --build
```
4. Использование API доступно по ссылке: http://localhost:8000/docs

Доступны 4 эндоинта:
- /devices/{device_id}/data - POST: отправка данных с устройства
- /devices/{device_id}/data - GET: получение данных с устройства за определенный промежуток времени
- /devices/{device_id}/data/all - GET: получение агрегированных данных за все время
- /tasks/recalculate - POST: Запуск фоновой задачи через Celery. Этот триггер позволяет инициировать длительный процесс обработки данных асинхронно, не блокируя основной поток обработки HTTP-запросов. (Результат будет доступен в логах контейнера celery-worker)

5. Для проведения нагрузочного тестирования: http://localhost:8089

6. Просмотр логов доступен через Docker Desktop или через команду:
```bash
docker-compose logs -f app
docker-compose logs -f celery-worker
docker-compose logs -f tests
docker-compose logs -f db
```




