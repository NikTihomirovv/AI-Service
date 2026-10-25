
import logging
from pathlib import Path

from faster_whisper import WhisperModel

from config.dataclasses import WhisperConfig
from service.exceptions import AudioTranscriptionError


logger = logging.getLogger(__name__)


class WhisperClient:
    """Клиент для распознавания аудио через faster-whisper."""

    def __init__(self, config: WhisperConfig):
        self.config = config

        logger.info(
            "Загрузка модели Whisper: %s",
            config.name,
        )

        self.model = WhisperModel(
            model_size_or_path=config.name,
            device=config.device,
            compute_type=config.compute_type,
        )

    def transcribe(
        self,
        audio_path: Path,
        lyrics: str | None = None,
    ) -> list[dict]:
        """Распознаёт аудио с необязательной текстовой подсказкой."""

        try:
            segments, _ = self.model.transcribe(
                audio=str(audio_path),
                language=self.config.language,
                beam_size=self.config.beam_size,
                word_timestamps=True,
                vad_filter=False,
                initial_prompt=lyrics or None,
            )

            words = []

            for segment in segments:
                for word in segment.words or []:
                    words.append({
                        "word": word.word.strip(),
                        "start": round(word.start, 2),
                        "end": round(word.end, 2),
                    })

            return words

        except Exception as exc:
            logger.exception("Ошибка распознавания аудио через Whisper")
            raise AudioTranscriptionError(
                "Не удалось распознать аудиофайл"
            ) from exc

    
    def close(self) -> None:
        """Освобождает ресурсы клиента."""

        self.model = None
