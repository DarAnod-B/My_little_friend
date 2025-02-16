from assistant.commands.base import Command

class NextTrackCommand(Command):
    name = "next_track"
    aliases = ["следующий трек", "переключи песню"]

    def __init__(self, module):
        self.module = module  # Ссылка на модуль

    async def execute(self):
        """Переключает трек, если плеер включён"""
        if self.module.state["player"]:
            return "Переключаю трек"
        return "Музыка не играет, сначала включите плеер"