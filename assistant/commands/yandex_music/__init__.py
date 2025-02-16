from assistant.commands.base import BaseModule
from assistant.commands.yandex_music.activate_module import ActivateMusicCommand
from assistant.commands.yandex_music.stop_module import StopMusicCommand
from assistant.commands.yandex_music.play import PlayMusicCommand
from assistant.commands.yandex_music.next import NextTrackCommand

class Module(BaseModule):
    name = "yandex_music"
    flag_default = False  # По умолчанию модуль выключен

    def __init__(self):
        super().__init__()
        self.state["player"] = False  # Переменная состояния плеера
        self.register_command(ActivateMusicCommand(self))  # Команда включения
        self.register_command(StopMusicCommand(self))      # Команда выключения
        self.register_command(PlayMusicCommand(self))
        self.register_command(NextTrackCommand(self))