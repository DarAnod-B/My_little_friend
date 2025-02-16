from assistant.commands import load_modules
from assistant.modules.nlp.intent_parser import IntentParser
from assistant.modules.nlp.lemmatizer import Lemmatizer
from assistant.utils.logger import logger


class CommandHandler:
    def __init__(self):
        self.modules = load_modules()
        self.intent_parser = IntentParser()
        self.lemmatizer = Lemmatizer()  # Лемматизатор добавлен здесь

    async def handle(self, user_input):
        """Обрабатывает входящую команду."""
        # Лемматизируем текст команды
        lemmatized_text = self.lemmatizer.lemmatize(user_input)
        logger.debug(f"Лемматизированный текст: {lemmatized_text}")

        # Определяем намерение
        command_name = self.intent_parser.predict_intent(lemmatized_text)

        if command_name:
            logger.debug(f"Распознанная команда: {command_name}")

            # Ищем команду в загруженных модулях
            for module in self.modules.values():
                for command in module.commands:
                    if command.name == command_name:
                        logger.debug(f"Найдена команда: {command.name}")

                        # Если это команда активации, всегда выполняем её
                        if command.name.startswith("activate_module_"):
                            logger.debug("Обнаружена команда активации, выполняем без проверки состояния модуля")
                            response = await command.execute()
                            logger.debug(f"Результат выполнения команды: {response}")
                            return response

                        # Для остальных команд проверяем активность модуля
                        if module.is_active:
                            response = await command.execute()
                            logger.debug(f"Результат выполнения команды: {response}")
                            return response
                        logger.warning(f"Модуль '{module.name}' неактивен.")
                        return f"Модуль '{module.name}' неактивен."

        # Если команда не найдена
        logger.warning("⚠️ Команда не распознана")
        return "Команда не найдена."