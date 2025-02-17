from assistant.commands.base import BaseModule
from assistant.commands.example_module.activate_module import ActivateMusicCommand
from assistant.commands.example_module.stop_module import StopMusicCommand
from assistant.commands.example_module.play import PlayMusicCommand
from assistant.commands.example_module.next import NextTrackCommand

class Module(BaseModule):
    name = "example_module"
    flag_default = False  # По умолчанию модуль выключен

    def __init__(self):
        super().__init__()
        self.state["player"] = False  # Переменная состояния плеера
        self.register_command(ActivateMusicCommand(self))  # Команда включения
        self.register_command(StopMusicCommand(self))      # Команда выключения
        self.register_command(PlayMusicCommand(self))
        self.register_command(NextTrackCommand(self))