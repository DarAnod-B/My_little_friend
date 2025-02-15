import json
from assistant.commands import load_commands
from assistant.modules.nlp.intent_parser import IntentParser
from assistant.utils.logger import logger

class CommandHandler:
    def __init__(self):
        self.commands = load_commands()
        self.intent_parser = IntentParser()

    async def handle(self, user_input):
        """Определяет и выполняет команду"""
        # 1️⃣ Проверка точного совпадения с командами
        command = self.commands.get(user_input.lower())
        if command:
            logger.info(f"✅ Найдена команда: {command.name}")
            return await command.execute() if hasattr(command, "execute") else command.execute()

        # 2️⃣ Если нет точного совпадения – анализируем текст
        intent = self.intent_parser.predict_intent(user_input)
        if intent and intent in self.commands:
            logger.info(f"🧠 Определено намерение: {intent}")
            return await self.commands[intent].execute()

        logger.warning(f"⚠️ Команда '{user_input}' не распознана.")
        return "Извините, я не понял команду."
    