from assistant.commands.base import Command

class PlayMusicCommand(Command):
    name = "play_music"
    aliases = ["играй дальше"]

    def __init__(self, module):
        self.module = module  # Ссылка на модуль

    async def execute(self):
        """Включает музыку"""
        if not self.module.state["player"]:
            self.module.state["player"] = "Музыкальный плеер запущен"
        return "Музыка играет"