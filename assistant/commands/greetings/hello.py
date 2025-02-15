from assistant.commands.base import Command

class HelloCommand(Command):
    name = "hello"
    
    async def execute(self, *args, **kwargs):  # Делаем асинхронным
        return "Привет! Чем могу пом+очь?"