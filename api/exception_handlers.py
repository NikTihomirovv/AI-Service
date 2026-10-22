
import logging

from fastapi import Request
from fastapi.responses import JSONResponse

from service.exceptions import (
    TextModelError,
    ImageModelError,
)


logger = logging.getLogger(__name__)


def text_model_error_handler(
    request: Request,
    exc: TextModelError,
) -> JSONResponse:
    """Обрабатывает ошибки текстовой модели."""

    logger.error("Text model error: %s", exc)

    return JSONResponse(
        status_code=502,
        content={
            "error": "TEXT_MODEL_ERROR",
            "detail": str(exc),
        },
    )


def image_model_error_handler(
    request: Request,
    exc: ImageModelError,
) -> JSONResponse:
    """Обрабатывает ошибки модели изображений."""

    logger.error("Image model error: %s", exc)

    return JSONResponse(
        status_code=502,
        content={
            "error": "IMAGE_MODEL_ERROR",
            "detail": str(exc),
        },
    )
