
from fastapi import FastAPI

from api.exception_handlers import (audio_transcription_error_handler,
                                    image_model_error_handler,
                                    text_model_error_handler)
from api.routes.generation import router as generation_router
from api.routes.transcription import router as transcription_router
from config.logging import setup_logging
from service.exceptions import (AudioTranscriptionError, ImageModelError,
                                TextModelError)

setup_logging()


app = FastAPI(
    title="AI-Service",
    description="API для генерации текста и изображений",
    version="0.1.0",
)


app.add_exception_handler(
    TextModelError,
    text_model_error_handler,
)

app.add_exception_handler(
    ImageModelError,
    image_model_error_handler,
)

app.add_exception_handler(
    AudioTranscriptionError,
    audio_transcription_error_handler,
)


app.include_router(
    generation_router,
    prefix="/api/v1",
    tags=["Generation"],
)

app.include_router(
    transcription_router,
    prefix="/api/v1",
    tags=["Transcription"],
)


@app.get("/health")
def health():
    """Проверяет доступность API-сервиса."""
    return {"status": "ok"}
