import importlib
import pkgutil
import inspect
import os
from assistant.commands.base import Command  # Импортируем базовый класс

def load_commands():
    """Автоматически загружает все команды из папки `commands/` (включая подпапки)."""
    commands = {}
    package = "assistant.commands"  # Указываем корневой пакет

    # Получаем абсолютный путь к папке commands
    commands_dir = os.path.dirname(__file__)

    # Рекурсивно обходим все подпапки
    for finder, module_name, ispkg in pkgutil.walk_packages([commands_dir], prefix=f"{package}."):
        module = importlib.import_module(module_name)

        # Ищем классы, унаследованные от Command
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if issubclass(obj, Command) and obj is not Command:  # Исключаем базовый класс
                command_name = obj.name  # Получаем имя команды
                commands[command_name] = obj()  # Создаём экземпляр

    return commands