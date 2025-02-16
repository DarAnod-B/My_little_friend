from assistant.commands.base import Command

class ActivateMusicCommand(Command):
    name = "activate_module_music"
    aliases = ["запусти музыку", "включи музыку"]

    def __init__(self, module):
        self.module = module  # Ссылка на модуль

    async def execute(self):
        """Активация модуля и запуск плеера"""
        self.module.is_active = True  # Включаем модуль
        self.module.state["player"] = True  # Включаем плеер
        # return "Музыка запущена"