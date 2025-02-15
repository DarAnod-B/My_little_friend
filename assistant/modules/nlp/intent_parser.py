import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from assistant.modules.nlp.lemmatizer import Lemmatizer  # Импортируем лемматизатор
from assistant.utils.config import Config

class IntentParser:
    def __init__(self, model_path=Config.INTENTS_PATH):
        with open(model_path, "r", encoding="utf-8") as f:
            self.intents = json.load(f)

        self.lemmatizer = Lemmatizer() 
        self.vectorizer = CountVectorizer()
        self.classifier = MultinomialNB()

        self.train()

    def train(self):
        texts = []
        labels = []

        for intent, examples in self.intents.items():
            # Лемматизируем примеры команд перед обучением
            lemmatized_examples = [self.lemmatizer.lemmatize(text) for text in examples]
            texts.extend(lemmatized_examples)
            labels.extend([intent] * len(examples))

        X = self.vectorizer.fit_transform(texts)
        self.classifier.fit(X, labels)

    def predict_intent(self, text: str) -> str:
        """Определяет намерение пользователя."""
        text = self.lemmatizer.lemmatize(text)  # Лемматизируем ввод
        X = self.vectorizer.transform([text])
        return self.classifier.predict(X)[0]