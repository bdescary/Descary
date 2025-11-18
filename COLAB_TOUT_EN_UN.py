"""
🚀 GOOGLE BUSINESS REVIEWS SCRAPER - VERSION TOUT-EN-UN POUR COLAB

INSTRUCTIONS:
1. Allez sur https://colab.research.google.com
2. Créez un nouveau notebook
3. COPIEZ TOUT CE FICHIER dans une cellule
4. Modifiez les 2 lignes de configuration (lignes 25-26)
5. Cliquez sur Play ▶

Attendez 2-3 minutes et votre fichier CSV se téléchargera automatiquement!
"""

# ==================== INSTALLATION ====================
print("⏳ Installation en cours... (30-60 secondes)")
import subprocess
import sys

# Installer Chrome et dépendances
subprocess.run(["apt-get", "update", "-qq"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.run(["apt", "install", "-y", "chromium-chromedriver"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.run(["cp", "/usr/lib/chromium-browser/chromedriver", "/usr/bin"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.run([sys.executable, "-m", "pip", "install", "-q", "selenium", "vaderSentiment", "pandas"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print("✅ Installation terminée!\n")

# ==================== CONFIGURATION ====================
# ⚙️ MODIFIEZ CES 2 LIGNES SELON VOS BESOINS:
BUSINESS_NAME = "Café Olimpico Montreal"  # ← Nom du business à analyser
MAX_REVIEWS = 30  # ← Nombre de reviews à récupérer (max ~100)

# ==================== CODE DU SCRAPER ====================
import time
import re
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class SentimentAnalyzer:
    """Analyse le sentiment des commentaires"""
    def __init__(self):
        self.vader = SentimentIntensityAnalyzer()
        self.french_words = {
            'excellent': 4.0, 'parfait': 4.0, 'magnifique': 3.5, 'superbe': 3.5,
            'génial': 3.5, 'merveilleux': 3.5, 'top': 3.0, 'super': 2.5,
            'bon': 2.0, 'bien': 2.0, 'recommande': 3.0, 'bravo': 2.5,
            'mauvais': -2.5, 'horrible': -3.5, 'nul': -3.0, 'médiocre': -2.5,
            'décevant': -2.5, 'déçu': -2.5, 'catastrophique': -4.0,
        }

    def analyze(self, text):
        if not text:
            return 0.0, 'Neutre'

        score = self.vader.polarity_scores(text)['compound']
        words = text.lower().split()
        fr_scores = [self.french_words[w] for w in words if w in self.french_words]

        if fr_scores:
            score = max(-1.0, min(1.0, sum(fr_scores) / len(fr_scores) / 4.0))

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


class GoogleBusinessScraper:
    """Scraper pour Google Business Reviews"""
    def __init__(self):
        self.driver = None
        self.sentiment = SentimentAnalyzer()

    def setup(self):
        print("🔧 Démarrage du navigateur...")
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=options)
        print("✅ Navigateur prêt!")

    def scrape(self, business_name, max_reviews=50):
        if not self.driver:
            self.setup()

        url = f"https://www.google.com/maps/search/{business_name.replace(' ', '+')}"
        print(f"\n🔍 Recherche: {business_name}")

        self.driver.get(url)
        time.sleep(3)

        # Ouvrir l'onglet Avis
        try:
            btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Avis')]"))
            )
            btn.click()
            time.sleep(2)
            print("✅ Onglet Avis ouvert")
        except:
            print("⚠️ Onglet Avis non trouvé (peut-être déjà ouvert)")

        # Scroll pour charger plus de reviews
        print("📜 Chargement des reviews...")
        for i in range(10):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

        # Cliquer sur "Plus" pour voir les reviews complètes
        try:
            more_btns = self.driver.find_elements(By.CSS_SELECTOR, 'button[aria-label*="Plus"]')
            for btn in more_btns[:20]:
                try:
                    self.driver.execute_script("arguments[0].click();", btn)
                except:
                    pass
        except:
            pass

        # Extraire les reviews
        print("\n📊 Extraction des reviews...")
        reviews = []
        elements = self.driver.find_elements(By.CSS_SELECTOR, 'div.jftiEf')
        print(f"✅ {len(elements)} reviews trouvées!\n")

        for idx, elem in enumerate(elements[:max_reviews]):
            try:
                # Extraire les infos
                try:
                    name = elem.find_element(By.CSS_SELECTOR, 'div.d4r55').text
                except:
                    name = "Anonyme"

                try:
                    rating_elem = elem.find_element(By.CSS_SELECTOR, 'span[role="img"]')
                    rating_text = rating_elem.get_attribute('aria-label')
                    rating = int(re.search(r'(\d+)', rating_text).group(1))
                except:
                    rating = None

                try:
                    text = elem.find_element(By.CSS_SELECTOR, 'span.wiI7pd').text
                except:
                    text = ""

                try:
                    date = elem.find_element(By.CSS_SELECTOR, 'span.rsqaWe').text
                except:
                    date = ""

                # Analyser le sentiment
                sentiment_score, sentiment_label = self.sentiment.analyze(text)

                reviews.append({
                    'id': idx + 1,
                    'auteur': name,
                    'note': rating,
                    'date': date,
                    'commentaire': text,
                    'sentiment_score': sentiment_score,
                    'sentiment': sentiment_label
                })

                if (idx + 1) % 5 == 0:
                    print(f"   ✓ {idx + 1}/{max_reviews} extraites...")

            except:
                continue

        print(f"\n✅ {len(reviews)} reviews récupérées!")
        return reviews

    def export_csv(self, reviews, filename="google_reviews.csv"):
        if not reviews:
            print("❌ Aucune review à exporter")
            return

        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['id', 'auteur', 'note', 'date',
                                                   'commentaire', 'sentiment_score', 'sentiment'])
            writer.writeheader()
            writer.writerows(reviews)

        print(f"\n💾 Export réussi: {filename}")
        print(f"📊 {len(reviews)} reviews exportées")

        avg_rating = sum(r['note'] for r in reviews if r['note']) / len(reviews)
        print(f"⭐ Note moyenne: {avg_rating:.2f}/5")

    def close(self):
        if self.driver:
            self.driver.quit()


# ==================== EXÉCUTION ====================
print("="*60)
print("🚀 DÉMARRAGE DU SCRAPER")
print("="*60)

scraper = GoogleBusinessScraper()

try:
    # Scraper les reviews
    reviews = scraper.scrape(BUSINESS_NAME, MAX_REVIEWS)

    if reviews:
        # Exporter en CSV
        scraper.export_csv(reviews)

        # Afficher les statistiques
        print("\n" + "="*60)
        print("📈 STATISTIQUES")
        print("="*60)

        sentiments = {}
        for r in reviews:
            sentiments[r['sentiment']] = sentiments.get(r['sentiment'], 0) + 1

        print("\nRépartition des sentiments:")
        for sentiment, count in sorted(sentiments.items()):
            pct = (count / len(reviews)) * 100
            bar = "█" * int(pct / 5)
            print(f"  {sentiment:15} {bar} {count:3} ({pct:.1f}%)")

        # Télécharger le fichier
        print("\n📥 Téléchargement du fichier CSV...")
        from google.colab import files
        files.download('google_reviews.csv')
        print("✅ Téléchargement lancé! Vérifiez votre dossier Téléchargements.")

        # Afficher quelques exemples
        print("\n" + "="*60)
        print("📝 EXEMPLES DE REVIEWS")
        print("="*60)
        for review in reviews[:3]:
            print(f"\n{review['auteur']} - {review['note']}⭐ - {review['sentiment']}")
            comment = review['commentaire'][:100]
            if len(review['commentaire']) > 100:
                comment += "..."
            print(f"  \"{comment}\"")

    else:
        print("\n❌ Aucune review trouvée")
        print("💡 Vérifiez le nom du business et réessayez")

except Exception as e:
    print(f"\n❌ Erreur: {e}")
    print("\n💡 Conseils:")
    print("   - Vérifiez que le business existe sur Google Maps")
    print("   - Essayez avec le nom complet + ville")
    print("   - Réexécutez la cellule")

finally:
    scraper.close()
    print("\n" + "="*60)
    print("👋 TERMINÉ!")
    print("="*60)
