import asyncio
from assistant.core.task_manager import TaskManager
from assistant.core.state_manager import StateManager
from assistant.core.command_handler import CommandHandler
from assistant.modules.speech.wake_word import WakeWordDetector
from assistant.modules.speech.recorder import Recorder
from assistant.modules.speech.stt import SpeechProcessor
from assistant.modules.tts.pyttsx3_engine import TextToSpeech
from assistant.utils.logger import logger
from assistant.utils.config import Config

class Bot:
    def __init__(self):
        self.task_manager = TaskManager()
        self.state_manager = StateManager()
        self.command_handler = CommandHandler()
        self.wake_word_detector = WakeWordDetector(Config.WAKE_WORD)
        self.recorder = Recorder()
        self.tts = TextToSpeech()
        self.speech_processor = SpeechProcessor()  # Создаём объект SpeechProcessor

    async def start(self):
        logger.info("🤖 Бот запущен. Ожидание активации...")

        while True:
            if self.wake_word_detector.detect():  # Ожидание ключевой фразы
                logger.info("🎤 Голосовая команда активирована")
                self.recorder.record()  # Запись команды

                # Получаем текст и intent
                command_data = self.speech_processor.speech_to_text()
                command_text = command_data["text"]
                intent = command_data["intent"]

                if command_text:
                    logger.info(f"📝 Распознано: {command_text}")
                    logger.info(f"🤖 Определённый intent: {intent}")

                    # Передаём intent в CommandHandler
                    response = await self.command_handler.handle(intent)
                    self.tts.speak(response)  # Озвучивание ответа
                else:
                    logger.warning("⚠️ Команда не распознана")

if __name__ == "__main__":
    bot = Bot()
    asyncio.run(bot.start())