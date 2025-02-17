import pyaudio
import wave
import struct
import math
import time

from assistant.utils.logger import logger
from assistant.utils.config import Config


class Recorder:
    def __init__(self):
        self.RATE = 16000  # Частота дискретизации
        self.CHANNELS = 1  # Количество каналов (моно)
        self.FORMAT = pyaudio.paInt16  # Формат аудиоданных
        self.CHUNK = 1024  # Размер буфера
        self.TIMEOUT_LENGTH = 1.0  # Время ожидания тишины
        self.MAX_RECORD_LENGTH = 20 # Максимальное время произнесения команды
        self.THRESHOLD = 70000 # Пороговое значение RMS
        self.FILE_PATH = Config.COMMAND_FILE

        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.FORMAT, channels=self.CHANNELS, 
                                  rate=self.RATE, input=True, frames_per_buffer=self.CHUNK)
        

    def _rms(self, frame):
        count = len(frame) // 2
        shorts = struct.unpack(f"{count}h", frame)
        sum_squares = sum(sample * sample for sample in shorts)
        return math.sqrt(sum_squares / count) * 1000
    
    def calibrate_threshold(self, duration=1):
        """
        Измеряет уровень фонового шума и устанавливает порог громкости (THRESHOLD).
        duration — длительность измерения в секундах.
        """
        logger.info("🔊 Калибровка уровня шума...")
        noise_levels = []

        # Записываем 1 секунду фонового шума
        for _ in range(int(self.RATE / self.CHUNK * duration)):  
            data = self.stream.read(self.CHUNK)
            rms_value = self._rms(data)
            noise_levels.append(rms_value)

        avg_noise = sum(noise_levels) / len(noise_levels)  # Среднее значение RMS
        threshold = avg_noise * 1.5  # Умножаем на 1.5 для запаса

        logger.info(f"Установленный порог: {threshold:.2f}")
        return threshold

    def record(self):
        logger.info("🎤 Запись команды...")
        rec = []
        start_time = time.time()
        current = start_time
        end = start_time + self.TIMEOUT_LENGTH

        while current - start_time <= self.MAX_RECORD_LENGTH:  # Запись не дольше 5 секунд
            data = self.stream.read(self.CHUNK)
            rms_value = self._rms(data)

            logger.info(f"🔹 RMS: {rms_value:.2f} (Порог: {self.THRESHOLD:.2f})")

            if rms_value >= self.THRESHOLD:
                end = time.time() + self.TIMEOUT_LENGTH  # Продлеваем запись, если голос громкий

            rec.append(data)
            current = time.time()

            if current > end:  # Если время вышло, остановить запись
                break  

        with wave.open(self.FILE_PATH, "wb") as wf:
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
            wf.setframerate(self.RATE)
            wf.writeframes(b"".join(rec))

        logger.info("✅ Команда записана!")