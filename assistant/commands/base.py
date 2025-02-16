from abc import ABC, abstractmethod

class Command(ABC):
    name = ""
    
    @abstractmethod
    async def execute(self, *args, **kwargs):  # Добавляем async
        """Асинхронный метод выполнения команды"""
        pass

class BaseModule:
    name = ""  # Уникальное имя модуля
    flag_default = False  # Включен ли модуль по умолчанию

    def __init__(self):
        self.commands = []
        self.state = {}  # Переменные состояния
        self.is_active = self.flag_default  # Атрибут активности, инициализируется значением flag_default

    def register_command(self, command):
        """Добавляет команду в модуль"""
        self.commands.append(command)