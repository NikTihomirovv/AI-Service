import logging
import time
from pathlib import Path

from service.ai_clients.ai_client_protocols import (
    AudioTranscriptionClientProtocol,
)


logger = logging.getLogger(__name__)


class TranscriptionService:
    """Сервис распознавания аудио."""

    def __init__(self, client: AudioTranscriptionClientProtocol):
        self.client = client

    def transcribe(
        self,
        audio_path: Path,
        lyrics: str | None = None,
    ) -> list[dict]:
        """Распознаёт аудио через выбранную модель."""

        start = time.perf_counter()

        logger.info("Начало распознавания аудио")

        try:
            result = self.client.transcribe(
                audio_path=audio_path,
                lyrics=lyrics,
            )
        except Exception:
            logger.exception("Ошибка распознавания аудио")
            raise

        duration = time.perf_counter() - start

        logger.info(
            "Распознавание завершено за %.2f сек.",
            duration,
        )

        return result