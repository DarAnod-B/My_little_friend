import os
from dotenv import load_dotenv

# Загружаем переменные из файла .env
load_dotenv()

class Config:
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL")
    VOSK_MODEL_PATH = os.getenv("VOSK_MODEL_PATH")
    COMMAND_FILE = os.getenv("COMMAND_FILE")
    WAKE_WORD = os.getenv("WAKE_WORD")
    INTENTS_PATH = os.getenv("INTENTS_PATH")
    VOICE = os.getenv("VOICE")
    LOGS_DATA_PATH = os.getenv("LOGS_DATA_PATH")


