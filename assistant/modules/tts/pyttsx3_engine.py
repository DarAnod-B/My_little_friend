import pyttsx3
from assistant.utils.config import Config

class TextToSpeech:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 240)
        self.voices = self.engine.getProperty('voices')
        for voice in self.voices:
            if Config.VOICE in voice.name:
                self.engine.setProperty('voice', voice.id)


    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

if __name__ == "__main__":
    tts = TextToSpeech()
    tts.speak("Всё функционирует в штатном режиме")   