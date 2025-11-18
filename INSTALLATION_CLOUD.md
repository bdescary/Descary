# 🌐 Installation sur Plateformes Cloud

Ce guide explique comment utiliser le Google Business Reviews Scraper sur différentes plateformes cloud.

## ❌ Plateformes NON compatibles

- **OneCompiler**: Ne supporte pas Selenium/Chrome
- **Repl.it** (version gratuite): Limitations avec Selenium
- **CodePen, JSFiddle**: Environnements frontend uniquement

## ✅ Plateformes COMPATIBLES

### 1. Google Colab (⭐ RECOMMANDÉ - Gratuit)

**Avantages**: Gratuit, Chrome préinstallé, GPU disponible, facile à utiliser

**Instructions détaillées**:

#### Étape 1: Créer un notebook
1. Allez sur https://colab.research.google.com
2. Cliquez sur "Nouveau notebook"

#### Étape 2: Installer les dépendances (Cellule 1)
```python
# Installation de Chrome et ChromeDriver
!apt-get update
!apt install -y chromium-chromedriver
!cp /usr/lib/chromium-browser/chromedriver /usr/bin

# Installation des packages Python
!pip install selenium beautifulsoup4 vaderSentiment textblob pandas
```

#### Étape 3: Créer sentiment_analyzer.py (Cellule 2)
```python
%%writefile sentiment_analyzer.py
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
from typing import Tuple

class SentimentAnalyzer:
    def __init__(self):
        self.vader_analyzer = SentimentIntensityAnalyzer()
        self.french_sentiment_words = {
            'excellent': 4.0, 'parfait': 4.0, 'magnifique': 3.5,
            'superbe': 3.5, 'génial': 3.5, 'bon': 2.0, 'bien': 2.0,
            'mauvais': -2.5, 'horrible': -3.5, 'nul': -3.0,
            'médiocre': -2.5, 'décevant': -2.5, 'déçu': -2.5,
        }

    def analyze(self, text: str) -> Tuple[float, str]:
        if not text:
            return 0.0, 'Neutre'

        score = self.vader_analyzer.polarity_scores(text)['compound']

        # Ajuster avec mots français
        words = text.lower().split()
        fr_scores = [self.french_sentiment_words[w] for w in words
                     if w in self.french_sentiment_words]
        if fr_scores:
            score = sum(fr_scores) / len(fr_scores) / 4.0

        # Label
        if score >= 0.5:
            label = 'Très Positif'
        elif score >= 0.1:
            label = 'Positif'
        elif score > -0.1:
            label = 'Neutre'
        elif score > -0.5:
            label = 'Négatif'
        else:
            label = 'Très Négatif'

        return round(score, 3), label
```

#### Étape 4: Créer le scraper (Cellule 3)
```python
%%writefile scraper_colab.py
import time
import re
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from sentiment_analyzer import SentimentAnalyzer

class GoogleBusinessScraper:
    def __init__(self):
        self.driver = None
        self.sentiment_analyzer = SentimentAnalyzer()

    def setup_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        self.driver = webdriver.Chrome(options=chrome_options)

    def scrape_reviews(self, search_query: str, max_reviews: int = 50):
        if not self.driver:
            self.setup_driver()

        url = f"https://www.google.com/maps/search/{search_query}"
        print(f"🔍 Scraping: {search_query}")
        self.driver.get(url)
        time.sleep(3)

        # Cliquer sur onglet Avis
        try:
            btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Avis')]"))
            )
            btn.click()
            time.sleep(2)
        except:
            pass

        # Scroll pour charger plus
        for i in range(10):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

        # Extraire reviews
        reviews_data = []
        elements = self.driver.find_elements(By.CSS_SELECTOR, 'div.jftiEf')

        for idx, elem in enumerate(elements[:max_reviews]):
            try:
                name = elem.find_element(By.CSS_SELECTOR, 'div.d4r55').text
                rating_elem = elem.find_element(By.CSS_SELECTOR, 'span[role="img"]')
                rating_text = rating_elem.get_attribute('aria-label')
                rating = int(re.search(r'(\d+)', rating_text).group(1))
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
                print(f"✓ Review {idx + 1}/{max_reviews}")
            except Exception as e:
                continue

        return reviews_data

    def export_to_csv(self, reviews, filename="reviews.csv"):
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['id', 'auteur', 'note', 'date',
                                                   'commentaire', 'sentiment_score', 'sentiment'])
            writer.writeheader()
            writer.writerows(reviews)
        print(f"✅ {len(reviews)} reviews → {filename}")

    def close(self):
        if self.driver:
            self.driver.quit()
```

#### Étape 5: Utiliser le scraper (Cellule 4)
```python
from scraper_colab import GoogleBusinessScraper

# Configuration
BUSINESS_NAME = "Café Olimpico Montreal"  # Modifiez ici
MAX_REVIEWS = 30  # Nombre de reviews à récupérer

# Scraping
scraper = GoogleBusinessScraper()
try:
    reviews = scraper.scrape_reviews(BUSINESS_NAME, MAX_REVIEWS)
    scraper.export_to_csv(reviews)

    # Statistiques
    if reviews:
        avg_rating = sum(r['note'] for r in reviews) / len(reviews)
        print(f"\n📊 RÉSUMÉ")
        print(f"Total: {len(reviews)} reviews")
        print(f"Note moyenne: {avg_rating:.2f}⭐")

        sentiments = {}
        for r in reviews:
            sentiments[r['sentiment']] = sentiments.get(r['sentiment'], 0) + 1
        print("\nSentiments:")
        for sent, count in sentiments.items():
            print(f"  {sent}: {count}")

    # Télécharger le CSV
    from google.colab import files
    files.download('reviews.csv')

finally:
    scraper.close()
```

**Résultat**: Le fichier CSV sera téléchargé automatiquement!

---

### 2. Replit (Hacker Plan - $7/mois)

**Avantages**: IDE complet, collaboration, toujours en ligne

**Instructions**:
1. Créez un compte sur https://replit.com
2. Créez un nouveau Repl Python
3. Uploadez les fichiers du projet
4. Installez Chrome via Nix:
```bash
# Dans replit.nix
{ pkgs }: {
  deps = [
    pkgs.chromium
    pkgs.chromedriver
  ];
}
```
5. Lancez `python google_business_scraper.py`

---

### 3. PythonAnywhere (Gratuit avec limitations)

**Avantages**: Hébergement Python gratuit

**Limitations**: Pas de Selenium dans la version gratuite

**Alternative**: Utilisez l'API Google Places si disponible

---

### 4. AWS EC2 / Google Cloud / DigitalOcean

**Pour utilisateurs avancés**

**Instructions générales**:
```bash
# 1. Se connecter au serveur
ssh user@your-server

# 2. Installer Python et dépendances
sudo apt update
sudo apt install python3-pip chromium-browser chromium-chromedriver

# 3. Cloner le projet
git clone <your-repo>
cd Descary

# 4. Installer les packages Python
pip3 install -r requirements.txt

# 5. Lancer le scraper
python3 google_business_scraper.py
```

---

### 5. Kaggle Notebooks (Gratuit)

**Avantages**: Gratuit, similaire à Colab

**Instructions**:
1. Allez sur https://www.kaggle.com/code
2. Créez un nouveau notebook
3. Suivez les mêmes étapes que Google Colab ci-dessus
4. Activez Internet dans les paramètres du notebook

---

## 💻 Installation LOCALE (Recommandé pour usage régulier)

### Windows
```bash
# Installer Python depuis python.org
# Ouvrir PowerShell/CMD
pip install -r requirements.txt
python google_business_scraper.py
```

### macOS
```bash
# Installer Homebrew si nécessaire
brew install python3
pip3 install -r requirements.txt
python3 google_business_scraper.py
```

### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3-pip chromium-browser chromium-chromedriver
pip3 install -r requirements.txt
python3 google_business_scraper.py
```

---

## 📝 Résumé des options

| Plateforme | Gratuit | Difficulté | Recommandé |
|------------|---------|------------|------------|
| **Google Colab** | ✅ Oui | ⭐ Facile | ✅ **OUI** |
| Kaggle | ✅ Oui | ⭐ Facile | ✅ Oui |
| Local (PC/Mac) | ✅ Oui | ⭐⭐ Moyen | ✅ Oui |
| Replit Hacker | ❌ $7/mois | ⭐⭐ Moyen | 🤔 Si besoin |
| AWS/GCP | ❌ Payant | ⭐⭐⭐ Difficile | 🤔 Si pro |
| OneCompiler | ❌ - | - | ❌ **NON** |
| PythonAnywhere | ⚠️ Limité | ⭐⭐ Moyen | ❌ Non |

---

## 🆘 Besoin d'aide?

- **Option recommandée #1**: Utilisez Google Colab (gratuit, facile)
- **Option recommandée #2**: Installez localement sur votre PC

Pour toute question, consultez le README.md principal du projet.
