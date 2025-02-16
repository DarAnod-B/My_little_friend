from assistant.modules.speech.wake_word import WakeWordDetector
from assistant.modules.speech.recorder import Recorder
from assistant.core.command_handler import CommandHandler
from assistant.modules.speech.stt import SpeechProcessor
from assistant.utils.logger import logger
from assistant.modules.tts.pyttsx3_engine import TextToSpeech


class Bot:
    def __init__(self):
        self.wake_word_detector = WakeWordDetector()  # Обнаружение ключевой фразы
        self.recorder = Recorder()  # Запись аудио
        self.speech_processor = SpeechProcessor()  # Преобразование речи в текст
        self.command_handler = CommandHandler()  # Обработка команд
        self.tts = TextToSpeech()  # TTS-движок


    async def start(self):
        logger.info("🤖 Бот запущен. Ожидание активации...")

        while True:
            # Ожидание ключевой фразы
            if self.wake_word_detector.detect():
                logger.info("🔹 Активирован по ключевой фразе!")

                # Запись команды
                self.recorder.record()

                # Преобразование речи в текст
                user_input = self.speech_processor.speech_to_text()
                logger.info(f"📝 Распознано: {user_input}")

                # Обработка команды
                response = await self.command_handler.handle(user_input)
                logger.info(f"🤖 Ответ: {response}")

                if response:  # Если есть ответ
                    self.tts.speak(response)  # Озвучиваем его
