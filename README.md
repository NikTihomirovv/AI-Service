AI-Service
Микросервис на Python + FastAPI для работы с локальными и внешними AI-моделями. Предоставляет REST API для генерации текста и изображений, а также распознавания аудио с пословными таймкодами.
Возможности
- Генерация текста через локальную Ollama (DeepSeek-R1 7B).
- Генерация изображений через Pollinations с возвратом Base64.
- Распознавание речи и вокала через faster-whisper.
- Возврат слов с временными метками start и end.
- Необязательная текстовая подсказка lyrics для распознавания песен.
- Конфигурация через YAML и переменные окружения.
- Разделение на API, сервисный слой и AI-клиенты с использованием Protocol и Dependency Injection.
- Логирование, обработка ошибок, запуск через Docker Compose.
- Поддержка NVIDIA GPU для Ollama.
Важно: lyrics передаётся Whisper как initial_prompt — это подсказка для распознавания, не forced alignment. Точное выравнивание готового текста песни по аудио пока не реализовано. Для пения возможны пропуски, неверные слова и неточные или нулевые длительности.

Технологии
- Python 3.12, FastAPI, Pydantic, Uvicorn
- Ollama, DeepSeek-R1 7B
- Pollinations, Requests
- faster-whisper 1.2.1, PyAV 15.1.0
- PyYAML, python-multipart
- Docker, Docker Compose
Архитектура
Client Application
       |
       v
     FastAPI
       |
       +---------------------------+
       |                           |
       v                           v
Generation endpoints       /audio/transcribe
       |                           |
       v                           v
GenerationService         TranscriptionService
       |                           |
       +---------------+           v
       |               |       WhisperClient
       v               v           |
  OllamaClient   PollinationsClient v
       |               |       faster-whisper
       v               v
   Local LLM       Image API
Слои проекта:
- API — маршруты, схемы запросов и ответов, зависимости и обработчики ошибок.
- Service — бизнес-логика и измерение времени выполнения.
- AI Clients — адаптеры конкретных моделей и провайдеров.
- Config — конфигурация приложения.
Структура проекта
AI-Service/
├── api/
│   ├── dependencies.py
│   ├── exception_handlers.py
│   ├── routes/
│   │   ├── generation.py
│   │   └── transcription.py
│   └── schemas/
│       ├── generation.py
│       └── transcription.py
├── config/
│   ├── config.yaml
│   ├── dataclasses.py
│   ├── loader.py
│   └── logging.py
├── service/
│   ├── ai_clients/
│   │   ├── ai_client_protocols.py
│   │   ├── ollama_client.py
│   │   ├── pollinations_client.py
│   │   └── whisper_client.py
│   ├── exceptions.py
│   ├── generation_service.py
│   └── transcription_service.py
├── .env.example
├── .dockerignore
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── main.py
├── requirements.txt
└── README.md
Установка и запуск
Требования
- Docker Desktop и Docker Compose.
- Для работы Ollama с GPU — совместимая NVIDIA GPU, драйверы и настроенный GPU-доступ в Docker/WSL2.
- Доступ в интернет для первой загрузки моделей.
1. Клонирование и настройка
git clone <repository-url>
cd AI-Service
Создайте .env на основе .env.example:
OLLAMA_BASE_URL=http://ollama:11434
Остальные параметры находятся в config/config.yaml.
2. Запуск
docker compose up -d --build
Загрузите модель Ollama при первом запуске:
docker compose exec ollama ollama pull deepseek-r1:7b
Модель Whisper загружается автоматически при первом обращении к эндпоинту транскрипции. Её кэш сохраняется в Docker volume whisper_cache.
3. Проверка
- Swagger UI: http://localhost:8001/docs
- Health check: http://localhost:8001/health
docker compose ps
docker compose logs -f ai-service
Остановка:
docker compose down
API
Генерация текста
POST /api/v1/text/generate
{
  "prompt": "Напиши короткую историю о космосе."
}
Ответ:
{
  "text": "Сгенерированный текст..."
}
Генерация изображения
POST /api/v1/images/generate
{
  "prompt": "Cinematic mountain landscape at sunset",
  "width": 1024,
  "height": 1024
}
Ответ:
{
  "image_base64": "<base64-encoded-image>"
}
Распознавание аудио
POST /api/v1/audio/transcribe

Тип запроса: multipart/form-data.
- file — обязательный аудиофайл.
- lyrics — необязательная строка с текстом песни; используется как подсказка Whisper.
Пример запроса:
curl -X POST "http://localhost:8001/api/v1/audio/transcribe" \
  -F "file=@vocals.wav" \
  -F "lyrics=Example lyrics for recognition"
Пример ответа:
{
  "words": [
    {"word": "Hello", "start": 1.2, "end": 1.55},
    {"word": "world", "start": 1.55, "end": 2.1}
  ]
}
В текущей конфигурации используется faster-whisper с пословными таймкодами (word_timestamps=True). Модель работает на CPU с int8; размер модели и язык задаются в YAML. Распознавание вокала, особенно в полной музыкальной композиции, может быть неточным.
Проверка работоспособности
GET /health
{
  "status": "ok"
}
Проверяется доступность FastAPI, но не готовность всех AI-моделей.
Конфигурация
Настройки находятся в config/config.yaml. Пример текущего блока Whisper:
whisper:
  name: "medium"
  device: "cpu"
  compute_type: "int8"
  language: "en"
  beam_size: 5
language: null включает автоматическое определение языка. Для песен на известном языке рекомендуется указывать его явно.

Для Ollama доступны название модели, URL, параметры генерации и таймауты. OLLAMA_BASE_URL можно переопределить переменной окружения.
Обработка ошибок и логирование
AI-ошибки обрабатываются централизованно. Пример:
{
  "error": "AUDIO_TRANSCRIPTION_ERROR",
  "detail": "Не удалось распознать аудиофайл"
}
Основные HTTP-коды:
- 200 — успешный запрос.
- 422 — ошибка валидации.
- 502 — ошибка AI-клиента.
- 500 — необработанная ошибка сервера.
Просмотр логов:
docker compose logs -f ai-service
Назначение и планы
AI-Service разрабатывается как самостоятельный микросервис для интеграции с другими приложениями:
- VideoMaker — генерация визуальных материалов и синхронизация текста с аудио для lyric video.
- PostGenerator — генерация текста и изображений для социальных сетей.
Планируемые улучшения:
- Forced alignment для точного сопоставления предоставленного текста песни с аудио.
- Проверка качества и корректировка проблемных таймкодов.
- Дополнительные AI-провайдеры и оптимизация производительности.
- Актуализация документации и автоматические тесты.
Статус
Версия: 0.1.0 (MVP).

Реализованы генерация текста, генерация изображений и базовая транскрипция аудио. Forced alignment ещё не реализован.