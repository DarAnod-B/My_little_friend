import importlib
import pkgutil
import os
from assistant.commands.base import BaseModule

def load_modules():
    """Автоматически загружает модули и команды из `commands/`"""
    modules = {}

    # Получаем путь к папке `commands`
    commands_dir = os.path.dirname(__file__)

    # Перебираем все подпапки в `commands/`
    for _, module_name, ispkg in pkgutil.iter_modules([commands_dir]):
        if ispkg:  # Загружаем только директории (модули)
            module_path = f"assistant.commands.{module_name}"
            module = importlib.import_module(f"{module_path}")
            
            if hasattr(module, "Module"):  # Проверяем, есть ли класс Module
                instance = module.Module()
                modules[module_name] = instance

    return modules