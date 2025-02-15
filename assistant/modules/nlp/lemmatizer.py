import spacy
from spacy.cli import download

class Lemmatizer:
    """Лемматизация текста через spaCy."""

    def __init__(self, lang="ru_core_news_sm"):
        try:
            self.nlp = spacy.load(lang)
        except OSError:
            print(f"⚠️ Модель {lang} не найдена! Устанавливаем автоматически...")
            download(lang)  # Загружаем модель
            self.nlp = spacy.load(lang)  # Загружаем снова после установки

    def lemmatize(self, text):
        """Приводит слова к начальной форме, удаляя стоп-слова."""
        text = str(text)  # Преобразуем в строку, если это numpy.str_
        doc = self.nlp(text)
        
        # Проверяем наличие is_stop, чтобы избежать ошибок
        return " ".join([token.lemma_ for token in doc if not getattr(token, "is_stop", False)])