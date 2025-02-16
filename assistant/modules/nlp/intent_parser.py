from assistant.modules.nlp.lemmatizer import Lemmatizer
from assistant.commands import load_modules
from assistant.utils.logger import logger


class IntentParser:
    def __init__(self):
        self.lemmatizer = Lemmatizer()  # Лемматизатор для нормализации текста
        self.commands = {}  # Список команд
        self.load_commands()  # Загружаем команды

    def load_commands(self):
        """Загружаем команды из модулей"""
        modules = load_modules()  # Загружаем команды из модулей
        for module in modules.values():
            for command in module.commands:
                self.commands[command.name] = command  # Сохраняем команду в словаре

    def predict_intent(self, text: str) -> str:
        """Определяет намерение пользователя на основе ключевых слов."""
        text = self.lemmatizer.lemmatize(text)  # Лемматизируем текст команды
        logger.debug(f"Лемматизированный текст: {text}")

        for command_name, command in self.commands.items():
            logger.debug(f"Проверка команды: {command_name}")
            for alias in command.aliases:
                alias = self.lemmatizer.lemmatize(alias)  # Лемматизируем синоним
                logger.debug(f"Лемматизированный синоним: {alias}")
                alias_words = alias.split()  # Разбиваем синоним на слова
                if all(word in text for word in alias_words):  # Проверяем, есть ли все слова синонима в тексте
                    logger.debug(f"Найдено совпадение: {command_name} (синоним: {alias})")
                    return command_name  # Если нашли совпадение, возвращаем имя команды

        logger.debug("Команда не распознана")
        return None  # Если команда не распознана