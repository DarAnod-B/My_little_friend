from assistant.commands.base import Command
from assistant.modules.api.ai_bot import OpenRouterAI
from assistant.modules.speech.stt import SpeechProcessor
from assistant.modules.tts.pyttsx3_engine import TextToSpeech


class AskAiCommand(Command):
    name = "ask_ai"
    aliases = ["ответь на вопрос", "у меня вопрос"]

    def __init__(self, module):
        self.module = module  # Ссылка на модуль
        self.ai_model = OpenRouterAI()
        self.stt = SpeechProcessor()
        self.tts = TextToSpeech()

    async def execute(self):
        """Активация модуля и запуск плеера"""
        question = self.stt.speech_to_text()
        prompt = f"""Ответь на вопрос не более 100 слов, а так если используешь дробные значения пиши их тексом, 
                    не используй языки разметки, пиши таким образом, чтобы голосовай ассистент, легко мог произнести ответ: {question}"""

        response = await self.ai_model.ai_ask(prompt)

        self.tts.speak(response)
        return response
