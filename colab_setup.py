"""
Instructions pour utiliser le scraper sur Google Colab
Copiez ce code dans un notebook Google Colab (https://colab.research.google.com)
"""

# CELLULE 1: Installation des dépendances
"""
!apt-get update
!apt install -y chromium-chromedriver
!cp /usr/lib/chromium-browser/chromedriver /usr/bin
!pip install selenium beautifulsoup4 vaderSentiment textblob pandas webdriver-manager
"""

# CELLULE 2: Créer le fichier sentiment_analyzer.py
sentiment_analyzer_code = '''
"""Module d'analyse de sentiment"""
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
from typing import Tuple

class SentimentAnalyzer:
    def __init__(self):
        self.vader_analyzer = SentimentIntensityAnalyzer()
        self.french_sentiment_words = {
            'excellent': 4.0, 'parfait': 4.0, 'magnifique': 3.5, 'superbe': 3.5,
            'génial': 3.5, 'merveilleux': 3.5, 'extraordinaire': 4.0,
            'formidable': 3.5, 'incroyable': 3.5, 'fantastique': 3.5,
            'délicieux': 3.0, 'agréable': 2.5, 'bon': 2.0, 'bien': 2.0,
            'satisfait': 2.5, 'content': 2.5, 'recommande': 3.0, 'top': 3.0,
            'super': 2.5, 'bravo': 2.5, 'mauvais': -2.5, 'horrible': -3.5,
            'terrible': -3.5, 'nul': -3.0, 'catastrophique': -4.0,
            'affreux': -3.5, 'médiocre': -2.5, 'décevant': -2.5,
            'déçu': -2.5, 'déplorable': -3.5, 'lamentable': -3.5,
            'pitoyable': -3.0, 'insuffisant': -2.0, 'inacceptable': -3.0,
        }

    def detect_language(self, text: str) -> str:
        if not text:
            return 'en'
        try:
            blob = TextBlob(text)
            return blob.detect_language()
        except:
            return 'fr'

    def analyze_french(self, text: str) -> float:
        if not text:
            return 0.0
        words = text.lower().split()
        scores = [self.french_sentiment_words[w] for w in words if w in self.french_sentiment_words]
        if scores:
            return max(-1.0, min(1.0, sum(scores) / len(scores) / 4.0))
        return self.vader_analyzer.polarity_scores(text)['compound']

    def analyze_english(self, text: str) -> float:
        if not text:
            return 0.0
        return self.vader_analyzer.polarity_scores(text)['compound']

    def get_sentiment_label(self, score: float) -> str:
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
        if not text or text.strip() == "":
            return 0.0, 'Neutre'
        language = self.detect_language(text)
        if language == 'fr':
            score = self.analyze_french(text)
        else:
            score = self.analyze_english(text)
        label = self.get_sentiment_label(score)
        return round(score, 3), label
'''

"""
with open('sentiment_analyzer.py', 'w', encoding='utf-8') as f:
    f.write(sentiment_analyzer_code)
"""

# CELLULE 3: Version simplifiée du scraper pour Colab
colab_scraper = '''
import time
import re
from datetime import datetime
from typing import List, Dict
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from sentiment_analyzer import SentimentAnalyzer
import csv

class GoogleBusinessScraperColab:
    """Version Colab du scraper"""

    def __init__(self):
        self.driver = None
        self.sentiment_analyzer = SentimentAnalyzer()

    def setup_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(10)

    def scrape_reviews(self, search_query: str, max_reviews: int = 50):
        if not self.driver:
            self.setup_driver()

        url = f"https://www.google.com/maps/search/{search_query}"
        print(f"Accès à: {url}")
        self.driver.get(url)
        time.sleep(3)

        # Cliquer sur les avis
        try:
            reviews_tab = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Avis')]"))
            )
            reviews_tab.click()
            time.sleep(2)
        except:
            print("Onglet Avis non trouvé")

        # Scroll
        for _ in range(10):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

        # Extraire les reviews
        reviews_data = []
        review_elements = self.driver.find_elements(By.CSS_SELECTOR, 'div.jftiEf')

        for idx, elem in enumerate(review_elements[:max_reviews]):
            try:
                name = elem.find_element(By.CSS_SELECTOR, 'div.d4r55').text
                rating = self._extract_rating(elem)
                text = elem.find_element(By.CSS_SELECTOR, 'span.wiI7pd').text
                date = elem.find_element(By.CSS_SELECTOR, 'span.rsqaWe').text

                sentiment_score, sentiment_label = self.sentiment_analyzer.analyze(text)

                reviews_data.append({
                    'id': idx + 1,
                    'auteur': name,
                    'note': rating,
                    'date': date,
                    'commentaire': text,
                    'sentiment_score': sentiment_score,
                    'sentiment': sentiment_label
                })
                print(f"✓ Review {idx + 1}: {name} - {rating}⭐")
            except:
                continue

        return reviews_data

    def _extract_rating(self, elem):
        try:
            rating_elem = elem.find_element(By.CSS_SELECTOR, 'span[role="img"]')
            aria_label = rating_elem.get_attribute('aria-label')
            match = re.search(r'(\d+)', aria_label)
            return int(match.group(1)) if match else None
        except:
            return None

    def export_to_csv(self, reviews_data, filename="reviews.csv"):
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['id', 'auteur', 'note', 'date', 'commentaire', 'sentiment_score', 'sentiment'])
            writer.writeheader()
            writer.writerows(reviews_data)
        print(f"✅ {len(reviews_data)} reviews exportées dans {filename}")
        return filename

    def close(self):
        if self.driver:
            self.driver.quit()

# UTILISATION
scraper = GoogleBusinessScraperColab()
try:
    reviews = scraper.scrape_reviews("Café Olimpico Montreal", max_reviews=30)
    scraper.export_to_csv(reviews)

    # Télécharger le fichier
    from google.colab import files
    files.download('reviews.csv')
finally:
    scraper.close()
'''

print("INSTRUCTIONS POUR GOOGLE COLAB:")
print("="*60)
print("1. Allez sur https://colab.research.google.com")
print("2. Créez un nouveau notebook")
print("3. Copiez le code ci-dessus dans des cellules séparées")
print("4. Exécutez chaque cellule dans l'ordre")
print("5. Le fichier CSV sera téléchargé automatiquement")
