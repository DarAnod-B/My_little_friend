import json
import wave
import re
from assistant.utils.config import Config
from vosk import KaldiRecognizer, Model
from assistant.modules.nlp.lemmatizer import Lemmatizer
from assistant.modules.nlp.intent_parser import IntentParser


class SpeechProcessor:
    """Класс для обработки голосовых команд."""

    def __init__(self):
        self.model = Model(Config.VOSK_MODEL_PATH)  # Загружаем модель Vosk
        self.lemmatizer = Lemmatizer()  # Лемматизатор для нормализации текста
        self.intent_parser = IntentParser()  # Определение намерений

    def speech_to_text(self):
        """Переводит речь в текст с постобработкой."""
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
        text = self.clean_text(text)  # Чистим текст
        lemmatized_text = self.lemmatizer.lemmatize(text)  # Лемматизируем
        intent = self.intent_parser.predict_intent(lemmatized_text)  # Определяем намерение

        return {"text": lemmatized_text, "intent": intent}

    def clean_text(self, text):
        """Удаляет лишние символы и форматирует текст."""
        text = text.lower().strip()
        text = re.sub(r"[^а-яa-z0-9\s]", "", text)  # Убираем знаки препинания
        text = re.sub(r"\s+", " ", text)  # Убираем лишние пробелы
        return text