
from typing import Protocol


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
