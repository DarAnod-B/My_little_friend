import pyaudio
from vosk import KaldiRecognizer, Model, SetLogLevel
from assistant.utils.config import Config
from assistant.utils.logger import logger

SetLogLevel(-1)

RATE = 16000
CHUNK = 1024

class WakeWordDetector:
    def __init__(self, wake_word=Config.WAKE_WORD):
        self.model = Model(Config.VOSK_MODEL_PATH)
        self.recognizer = KaldiRecognizer(self.model, RATE)
        self.wake_word = wake_word.lower()

    def detect(self):
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNK)
        stream.start_stream()

        logger.info("🎤 Ожидание ключевой фразы...")

        while True:
            data = stream.read(CHUNK)
            if not data:
                break

            if self.recognizer.AcceptWaveform(data):
                result = self.recognizer.Result()
                if self.wake_word in result.lower():
                    logger.info("🔹 Активация!")
                    return True