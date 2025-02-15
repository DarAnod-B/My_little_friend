from abc import ABC, abstractmethod

class Command(ABC):
    name = ""
    
    @abstractmethod
    async def execute(self, *args, **kwargs):  # Добавляем async
        """Асинхронный метод выполнения команды"""
        pass