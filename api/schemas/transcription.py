from pydantic import BaseModel


class TranscribedWord(BaseModel):
    """Распознанное слово с таймкодами."""

    word: str
    start: float
    end: float


class TranscriptionResponse(BaseModel):
    """Результат распознавания аудио."""

    words: list[TranscribedWord]