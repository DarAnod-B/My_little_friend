import json
import wave
import re
from assistant.utils.config import Config
from vosk import KaldiRecognizer, Model
from assistant.utils.logger import logger
from assistant.modules.speech.recorder import Recorder


class SpeechProcessor:
    """Класс для обработки голосовых команд."""

    def __init__(self):
        self.model = Model(Config.VOSK_MODEL_PATH)  # Загружаем модель Vosk
        self.recorder = Recorder() 

    def speech_to_text(self):
        """Переводит речь в текст с постобработкой."""
        self.recorder.record()
        
        wf = wave.open(Config.COMMAND_FILE, "rb")
        rec = KaldiRecognizer(self.model, wf.getframerate())

        result = []
        last_empty = False

        while True:
            data = wf.readframes(wf.getframerate())
            if len(data) == 0:
                break

            if rec.AcceptWaveform(data):
                res = json.loads(rec.Result())
                text = res["text"].strip()

                if text:
                    result.append(text)
                    last_empty = False
                elif not last_empty:
                    result.append("\n")  # Добавляем перенос строки между фразами
                    last_empty = True

        # Финальный результат Vosk
        res = json.loads(rec.FinalResult())
        if res["text"]:
            result.append(res["text"].strip())

        # Объединяем в строку и очищаем
        text = " ".join(result).strip()
        text = self.clean_text(text) 

        logger.debug(f"Распознанный текст: {text}")

        return text

    def clean_text(self, text):
        """Удаляет лишние символы и форматирует текст."""
        text = text.lower().strip()
        text = re.sub(r"\s+", " ", text)  # Убираем лишние пробелы
        return text