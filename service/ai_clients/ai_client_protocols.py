
from typing import Protocol
from pathlib import Path


class TextModelClientProtocol(Protocol):
    """Контракт для взаимодействия с текстовой моделью."""

    def generate(self, prompt: str) -> str:
        """Генерирует текст по запросу."""
        ...

    def close(self) -> None:
        """Освобождает ресурсы клиента."""
        ...


class ImageModelClientProtocol(Protocol):
    """Контракт для взаимодействия с моделью изображений."""

    def generate(
        self,
        prompt: str,
        resolution: tuple[int, int],
    ) -> str:
        """Генерирует изображение в формате Base64."""
        ...

    def close(self) -> None:
        """Освобождает ресурсы клиента."""
        ...


class AudioTranscriptionClientProtocol(Protocol):
    """Контракт для распознавания аудио."""

    def transcribe(
        self,
        audio_path: Path,
        lyrics: str | None = None,
        ) -> list[dict]:
        """Распознаёт аудио и возвращает слова с таймкодами."""
        ...

    def close(self) -> None:
        """Освобождает ресурсы клиента."""
        ...


