# AI-Service

Микросервис для генерации текста и изображений с использованием локальных и внешних AI-моделей.

Разработан на **Python + FastAPI**. Предоставляет единый REST API для взаимодействия с AI-провайдерами.

## Возможности

- Генерация текста через локальную Ollama.
- Генерация изображений через Pollinations.
- Единый HTTP API для других приложений.
- Конфигурация через YAML и переменные окружения.
- Dependency Injection и разделение бизнес-логики и AI-клиентов.
- Централизованная обработка ошибок и логирование.
- Запуск через Docker Compose.
- Поддержка NVIDIA GPU для Ollama.

## Технологии

- Python 3.12
- FastAPI
- Pydantic
- Ollama
- DeepSeek-R1 7B
- Pollinations
- Requests
- PyYAML
- Docker / Docker Compose

## Архитектура

```text
Client Application
        |
        v
     FastAPI
        |
        v
GenerationService
        |
        v
AI Client Protocol
        |
        +-------------------+
        |                   |
        v                   v
   OllamaClient     PollinationsClient
        |                   |
        v                   v
   Local LLM          Image API
```

Проект использует разделение на несколько уровней:

- **API** — HTTP-маршруты, схемы запросов и ответов.
- **Service** — сервисный слой генерации.
- **AI Clients** — взаимодействие с конкретными провайдерами.
- **Config** — конфигурация приложения.

Клиенты реализуют соответствующие интерфейсы `Protocol`, что позволяет заменять провайдеров без изменения сервисного слоя.

## Структура проекта

```text
AI-Service/
├── api/
│   ├── dependencies.py
│   ├── exception_handlers.py
│   ├── routes/
│   │   └── generation.py
│   └── schemas/
│       └── generation.py
├── config/
│   ├── config.yaml
│   ├── dataclasses.py
│   ├── loader.py
│   └── logging.py
├── service/
│   ├── ai_clients/
│   │   ├── ai_client_protocols.py
│   │   ├── ollama_client.py
│   │   └── pollinations_client.py
│   ├── exceptions.py
│   └── generation_service.py
├── .env.example
├── .dockerignore
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── main.py
├── requirements.txt
└── README.md
```

## Установка и запуск

### Требования

- Docker Desktop
- Docker Compose
- NVIDIA GPU с поддержкой CUDA — рекомендуется для локальных моделей
- WSL2 — для запуска Docker с GPU на Windows

### 1. Клонирование репозитория

```bash
git clone <repository-url>
cd AI-Service
```

### 2. Настройка окружения

Создайте `.env` на основе `.env.example`:

```env
OLLAMA_BASE_URL=http://ollama:11434
```

Остальные настройки находятся в `config/config.yaml`.

### 3. Запуск контейнеров

```bash
docker compose up -d --build
```

### 4. Загрузка текстовой модели

```bash
docker compose exec ollama ollama pull deepseek-r1:7b
```

Модель сохраняется в Docker volume и не требует повторной загрузки при обычном перезапуске контейнеров.

### 5. Проверка

Swagger UI:

`http://localhost:8001/docs`

Проверка FastAPI:

`http://localhost:8001/health`

Проверка контейнеров:

```bash
docker compose ps
```

Проверка использования GPU:

```bash
docker compose exec ollama ollama ps
```

## API

### Генерация текста

**POST** `/api/v1/text/generate`

Запрос:

```json
{
  "prompt": "Напиши короткую историю о космосе."
}
```

Ответ:

```json
{
  "text": "Сгенерированный текст..."
}
```

### Генерация изображения

**POST** `/api/v1/images/generate`

Запрос:

```json
{
  "prompt": "Cinematic mountain landscape at sunset",
  "width": 1024,
  "height": 1024
}
```

Ответ:

```json
{
  "image_base64": "<base64-encoded-image>"
}
```

Изображение возвращается в виде строки Base64.

Доступность генерации изображений зависит от используемого API Pollinations.

### Проверка работоспособности

**GET** `/health`

Ответ:

```json
{
  "status": "ok"
}
```

Этот маршрут проверяет работу FastAPI, но не готовность AI-моделей.

## Обработка ошибок

Для ошибок AI-провайдеров предусмотрены структурированные JSON-ответы.

Пример:

```json
{
  "error": "TEXT_MODEL_ERROR",
  "detail": "Ошибка при генерации текста через Ollama"
}
```

Основные HTTP-коды:

- `200` — успешный запрос.
- `422` — ошибка валидации входных данных.
- `502` — ошибка взаимодействия с AI-провайдером.
- `500` — необработанная внутренняя ошибка.

## Логирование

Сервис записывает информацию о начале и завершении генерации, продолжительности выполнения и возникающих ошибках.

Просмотр логов:

```bash
docker compose logs -f ai-service
```

## Конфигурация

Параметры моделей задаются в `config/config.yaml`.

Для Ollama поддерживаются настройки:

- Название модели.
- Адрес сервера.
- Temperature.
- Top P.
- Максимальное количество генерируемых токенов.
- Таймауты подключения и чтения.

Адрес Ollama может быть переопределён через `OLLAMA_BASE_URL`.

## Назначение

AI-Service разрабатывается как самостоятельный микросервис, который можно использовать в разных приложениях.

Планируемые интеграции:

- **VideoMaker** — генерация визуальных материалов для видео.
- **PostGenerator** — генерация текстов и изображений для публикаций в социальных сетях.

## Текущий статус

**Версия:** 0.1.0 (MVP)

Реализована базовая инфраструктура генерации текста и изображений.

Планируемые улучшения:

- Поддержка дополнительных AI-провайдеров.
- Расширение настроек генерации.
- Оптимизация локальных моделей.
- Интеграция с клиентскими приложениями.
