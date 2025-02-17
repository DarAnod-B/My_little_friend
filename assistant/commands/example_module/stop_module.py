from assistant.commands.base import Command

class StopMusicCommand(Command):
    name = "stop_music"
    aliases = ["останови музыку", "выключи музыку"]

    def __init__(self, module):
        self.module = module  # Ссылка на модуль

    async def execute(self):
        """Выключение модуля и остановка плеера"""
        if self.module.state["player"]:  # Если плеер включён
            self.module.state["player"] = False  # Выключаем плеер
            self.module.is_active = False  # Выключаем модуль
            # return "Музыка остановлена"
        return "Музыка уже выключена"