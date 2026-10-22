
from pydantic import BaseModel, Field


class TextGenerationRequest(BaseModel):
    """Запрос на генерацию текста."""

    prompt: str = Field(min_length=1)


class TextGenerationResponse(BaseModel):
    """Ответ с результатом генерации текста."""

    text: str


class ImageGenerationRequest(BaseModel):
    """Запрос на генерацию изображения."""

    prompt: str = Field(min_length=1)
    width: int = Field(gt=0)
    height: int = Field(gt=0)


class ImageGenerationResponse(BaseModel):
    """Ответ с результатом генерации изображения."""

    image_base64: str
