
from typing import Annotated

from fastapi import APIRouter, Depends

from api.dependencies import (
    get_text_generation_service,
    get_image_generation_service,
)
from api.schemas.generation import (
    TextGenerationRequest,
    TextGenerationResponse,
    ImageGenerationRequest,
    ImageGenerationResponse,
)
from service.generation_service import (
    TextGenerationService,
    ImageGenerationService,
)


router = APIRouter()


@router.post(
    "/text/generate",
    response_model=TextGenerationResponse,
)
def generate_text(
    request: TextGenerationRequest,
    service: Annotated[
        TextGenerationService,
        Depends(get_text_generation_service),
    ],
) -> TextGenerationResponse:
    """Генерирует текст."""

    result = service.generate(request.prompt)

    return TextGenerationResponse(text=result)


@router.post(
    "/images/generate",
    response_model=ImageGenerationResponse,
)
def generate_image(
    request: ImageGenerationRequest,
    service: Annotated[
        ImageGenerationService,
        Depends(get_image_generation_service),
    ],
) -> ImageGenerationResponse:
    """Генерирует изображение."""

    result = service.generate(
        prompt=request.prompt,
        resolution=(request.width, request.height),
    )

    return ImageGenerationResponse(image_base64=result)
