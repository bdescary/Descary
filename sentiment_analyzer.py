"""
Module d'analyse de sentiment pour les reviews Google Business
Utilise VADER pour l'analyse de sentiment en français et en anglais
"""

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
from typing import Tuple


class SentimentAnalyzer:
    """Analyseur de sentiment pour les reviews"""

    def __init__(self):
        """Initialise l'analyseur de sentiment"""
        self.vader_analyzer = SentimentIntensityAnalyzer()

        # Dictionnaire de mots français pour améliorer l'analyse
        self.french_sentiment_words = {
            # Mots positifs
            'excellent': 4.0,
            'parfait': 4.0,
            'magnifique': 3.5,
            'superbe': 3.5,
            'génial': 3.5,
            'merveilleux': 3.5,
            'extraordinaire': 4.0,
            'formidable': 3.5,
            'incroyable': 3.5,
            'fantastique': 3.5,
            'délicieux': 3.0,
            'agréable': 2.5,
            'bon': 2.0,
            'bien': 2.0,
            'satisfait': 2.5,
            'content': 2.5,
            'recommande': 3.0,
            'top': 3.0,
            'super': 2.5,
            'bravo': 2.5,

            # Mots négatifs
            'mauvais': -2.5,
            'horrible': -3.5,
            'terrible': -3.5,
            'nul': -3.0,
            'catastrophique': -4.0,
            'affreux': -3.5,
            'médiocre': -2.5,
            'décevant': -2.5,
            'déçu': -2.5,
            'déplorable': -3.5,
            'lamentable': -3.5,
            'pitoyable': -3.0,
            'insuffisant': -2.0,
            'inacceptable': -3.0,
            'honteux': -3.5,
            'scandaleux': -3.5,
            'désastreux': -3.5,
            'pas': -1.0,
            'jamais': -1.5,
            'rien': -1.5,
        }

    def detect_language(self, text: str) -> str:
        """
        Détecte la langue du texte

        Args:
            text: Texte à analyser

        Returns:
            Code de langue ('fr' ou 'en')
        """
        if not text:
            return 'en'

        try:
            blob = TextBlob(text)
            return blob.detect_language()
        except:
            # Par défaut, on suppose que c'est du français
            return 'fr'

    def analyze_french(self, text: str) -> float:
        """
        Analyse de sentiment pour le français

        Args:
            text: Texte en français

        Returns:
            Score de sentiment (-1 à 1)
        """
        if not text:
            return 0.0

        words = text.lower().split()
        scores = []

        for word in words:
            if word in self.french_sentiment_words:
                scores.append(self.french_sentiment_words[word])

        if scores:
            # Moyenne des scores trouvés
            avg_score = sum(scores) / len(scores)
            # Normaliser entre -1 et 1
            return max(-1.0, min(1.0, avg_score / 4.0))

        # Si aucun mot français reconnu, utiliser VADER quand même
        return self.vader_analyzer.polarity_scores(text)['compound']

    def analyze_english(self, text: str) -> float:
        """
        Analyse de sentiment pour l'anglais avec VADER

        Args:
            text: Texte en anglais

        Returns:
            Score de sentiment (-1 à 1)
        """
        if not text:
            return 0.0

        scores = self.vader_analyzer.polarity_scores(text)
        return scores['compound']

    def get_sentiment_label(self, score: float) -> str:
        """
        Convertit un score de sentiment en label

        Args:
            score: Score de sentiment (-1 à 1)

        Returns:
            Label de sentiment
        """
        if score >= 0.5:
            return 'Très Positif'
        elif score >= 0.1:
            return 'Positif'
        elif score > -0.1:
            return 'Neutre'
        elif score > -0.5:
            return 'Négatif'
        else:
            return 'Très Négatif'

    def analyze(self, text: str) -> Tuple[float, str]:
        """
        Analyse le sentiment d'un texte

        Args:
            text: Texte à analyser

        Returns:
            Tuple (score, label) où:
            - score est un float entre -1 (très négatif) et 1 (très positif)
            - label est une description textuelle du sentiment
        """
        if not text or text.strip() == "":
            return 0.0, 'Neutre'

        # Détecter la langue
        language = self.detect_language(text)

        # Analyser selon la langue
        if language == 'fr':
            score = self.analyze_french(text)
        else:
            score = self.analyze_english(text)

        # Obtenir le label
        label = self.get_sentiment_label(score)

        return round(score, 3), label


def main():
    """Fonction de test pour l'analyseur de sentiment"""
    analyzer = SentimentAnalyzer()

    # Tests en français
    test_texts_fr = [
        "Excellent restaurant, service impeccable!",
        "Très déçu, qualité médiocre",
        "C'est bon mais rien d'exceptionnel",
        "Absolument catastrophique, je ne recommande pas du tout",
        "Magnifique expérience, je recommande vivement!"
    ]

    print("Tests en français:")
    print("="*60)
    for text in test_texts_fr:
        score, label = analyzer.analyze(text)
        print(f"Texte: {text}")
        print(f"Score: {score:.3f} | Sentiment: {label}\n")

    # Tests en anglais
    test_texts_en = [
        "Amazing food and great service!",
        "Terrible experience, would not recommend",
        "It was okay, nothing special",
        "Absolutely fantastic, best meal ever!",
        "Disappointing quality for the price"
    ]

    print("\nTests en anglais:")
    print("="*60)
    for text in test_texts_en:
        score, label = analyzer.analyze(text)
        print(f"Texte: {text}")
        print(f"Score: {score:.3f} | Sentiment: {label}\n")


if __name__ == "__main__":
    main()
