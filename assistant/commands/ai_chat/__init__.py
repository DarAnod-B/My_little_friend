from assistant.commands.base import BaseModule
from assistant.commands.ai_chat.ask_ai import AskAiCommand


class Module(BaseModule):
    name = "ai_chat"
    flag_default = True  # По умолчанию модуль выключен

    def __init__(self):
        super().__init__()
        self.register_command(AskAiCommand(self))  
