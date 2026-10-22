
from fastapi import FastAPI

from config.logging import setup_logging

from api.routes.generation import router as generation_router
from api.exception_handlers import (
    text_model_error_handler,
    image_model_error_handler,
)
from service.exceptions import (
    TextModelError,
    ImageModelError,
)


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


app.include_router(
    generation_router,
    prefix="/api/v1",
    tags=["Generation"],
)


@app.get("/health")
def health():
    """Проверяет доступность API-сервиса."""
    return {"status": "ok"}
