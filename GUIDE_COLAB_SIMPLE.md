# 🚀 Guide Ultra-Simple pour Google Colab

## Ce que vous allez faire

Vous allez copier-coller du code dans Google Colab (gratuit) et récupérer les reviews Google Business en CSV.

**Temps nécessaire**: 5-10 minutes
**Compétences requises**: Savoir copier-coller 😊

---

## Étape 1: Ouvrir Google Colab

1. Allez sur **https://colab.research.google.com**
2. Connectez-vous avec votre compte Google
3. Cliquez sur **"Nouveau notebook"** (bouton en haut à gauche)

Vous verrez une page blanche avec une case grise (c'est une "cellule" de code).

---

## Étape 2: Installer les outils (Cellule 1)

Dans la première cellule, **copiez-collez ce code**:

```python
# Installation de Chrome et des outils nécessaires
print("⏳ Installation en cours... (ça prend 30-60 secondes)")

!apt-get update -qq
!apt install -y chromium-chromedriver
!cp /usr/lib/chromium-browser/chromedriver /usr/bin
!pip install -q selenium beautifulsoup4 vaderSentiment textblob pandas

print("✅ Installation terminée!")
```

Ensuite:
- Cliquez sur le **bouton Play** (▶) à gauche de la cellule
- **OU** appuyez sur `Shift + Enter`

⏳ Attendez environ 1 minute que tout s'installe. Vous verrez défiler du texte.

---

## Étape 3: Créer l'analyseur de sentiment (Cellule 2)

Cliquez en bas de la première cellule, puis cliquez sur **"+ Code"** pour ajouter une nouvelle cellule.

**Copiez-collez ce code dans la cellule 2**:

```python
%%writefile sentiment_analyzer.py
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from typing import Tuple

class SentimentAnalyzer:
    def __init__(self):
        self.vader = SentimentIntensityAnalyzer()

        # Mots français avec leurs scores
        self.french_words = {
            'excellent': 4.0, 'parfait': 4.0, 'magnifique': 3.5, 'superbe': 3.5,
            'génial': 3.5, 'merveilleux': 3.5, 'extraordinaire': 4.0, 'top': 3.0,
            'formidable': 3.5, 'incroyable': 3.5, 'fantastique': 3.5, 'super': 2.5,
            'délicieux': 3.0, 'agréable': 2.5, 'bon': 2.0, 'bien': 2.0,
            'satisfait': 2.5, 'content': 2.5, 'recommande': 3.0, 'bravo': 2.5,
            'mauvais': -2.5, 'horrible': -3.5, 'terrible': -3.5, 'nul': -3.0,
            'catastrophique': -4.0, 'affreux': -3.5, 'médiocre': -2.5,
            'décevant': -2.5, 'déçu': -2.5, 'déplorable': -3.5,
            'lamentable': -3.5, 'pitoyable': -3.0, 'inacceptable': -3.0,
        }

    def analyze(self, text: str) -> Tuple[float, str]:
        if not text or text.strip() == "":
            return 0.0, 'Neutre'

        # Score de base avec VADER
        score = self.vader.polarity_scores(text)['compound']

        # Améliorer avec mots français
        words = text.lower().split()
        french_scores = [self.french_words[w] for w in words if w in self.french_words]

        if french_scores:
            score = sum(french_scores) / len(french_scores) / 4.0
            score = max(-1.0, min(1.0, score))

        # Déterminer le label
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

Cliquez sur **Play** (▶) pour exécuter.

---

## Étape 4: Créer le scraper (Cellule 3)

Ajoutez une nouvelle cellule et **copiez-collez ce code**:

```python
%%writefile google_scraper.py
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
        """Configure Chrome en mode invisible"""
        print("🔧 Configuration du navigateur...")
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        self.driver = webdriver.Chrome(options=options)
        print("✅ Navigateur prêt!")

    def scrape_reviews(self, business_name: str, max_reviews: int = 50):
        """Récupère les reviews d'un business"""
        if not self.driver:
            self.setup_driver()

        # Construire l'URL Google Maps
        url = f"https://www.google.com/maps/search/{business_name.replace(' ', '+')}"
        print(f"\n🔍 Recherche: {business_name}")
        print(f"📍 URL: {url}")

        self.driver.get(url)
        time.sleep(3)

        # Cliquer sur l'onglet "Avis"
        try:
            print("🔎 Recherche de l'onglet Avis...")
            reviews_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Avis')]"))
            )
            reviews_button.click()
            print("✅ Onglet Avis trouvé!")
            time.sleep(2)
        except:
            print("⚠️ Onglet Avis non trouvé, on continue quand même...")

        # Faire défiler pour charger plus de reviews
        print(f"📜 Chargement des reviews...")
        for i in range(10):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            if (i + 1) % 3 == 0:
                print(f"   Scroll {i + 1}/10...")

        # Cliquer sur les boutons "Plus" pour voir les reviews complètes
        try:
            more_buttons = self.driver.find_elements(By.CSS_SELECTOR, 'button[aria-label*="Plus"]')
            for btn in more_buttons[:20]:  # Limiter à 20 pour éviter de perdre du temps
                try:
                    self.driver.execute_script("arguments[0].click();", btn)
                except:
                    pass
        except:
            pass

        # Extraire les reviews
        print(f"\n📊 Extraction des reviews...")
        reviews_data = []

        try:
            review_elements = self.driver.find_elements(By.CSS_SELECTOR, 'div.jftiEf')
            print(f"✅ {len(review_elements)} reviews trouvées!")

            for idx, element in enumerate(review_elements[:max_reviews]):
                try:
                    # Nom de l'auteur
                    try:
                        name = element.find_element(By.CSS_SELECTOR, 'div.d4r55').text
                    except:
                        name = "Anonyme"

                    # Note (étoiles)
                    try:
                        rating_elem = element.find_element(By.CSS_SELECTOR, 'span[role="img"]')
                        rating_text = rating_elem.get_attribute('aria-label')
                        rating = int(re.search(r'(\d+)', rating_text).group(1))
                    except:
                        rating = None

                    # Commentaire
                    try:
                        text = element.find_element(By.CSS_SELECTOR, 'span.wiI7pd').text
                    except:
                        text = ""

                    # Date
                    try:
                        date = element.find_element(By.CSS_SELECTOR, 'span.rsqaWe').text
                    except:
                        date = ""

                    # Analyser le sentiment
                    sentiment_score, sentiment_label = self.sentiment_analyzer.analyze(text)

                    # Ajouter à la liste
                    reviews_data.append({
                        'id': idx + 1,
                        'auteur': name,
                        'note': rating,
                        'date': date,
                        'commentaire': text,
                        'sentiment_score': sentiment_score,
                        'sentiment': sentiment_label
                    })

                    # Afficher la progression
                    if (idx + 1) % 5 == 0:
                        print(f"   ✓ {idx + 1}/{max_reviews} reviews extraites...")

                except Exception as e:
                    continue

        except Exception as e:
            print(f"❌ Erreur: {e}")

        print(f"\n✅ Extraction terminée: {len(reviews_data)} reviews récupérées!")
        return reviews_data

    def export_to_csv(self, reviews, filename="google_reviews.csv"):
        """Exporte les reviews en CSV"""
        if not reviews:
            print("❌ Aucune review à exporter")
            return

        with open(filename, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['id', 'auteur', 'note', 'date', 'commentaire',
                         'sentiment_score', 'sentiment']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(reviews)

        print(f"\n💾 Export réussi!")
        print(f"📁 Fichier: {filename}")
        print(f"📊 Nombre de reviews: {len(reviews)}")

        # Statistiques rapides
        avg_rating = sum(r['note'] for r in reviews if r['note']) / len(reviews)
        print(f"⭐ Note moyenne: {avg_rating:.2f}/5")

    def close(self):
        """Ferme le navigateur"""
        if self.driver:
            self.driver.quit()
```

Cliquez sur **Play** (▶).

---

## Étape 5: Utiliser le scraper (Cellule 4)

**C'EST ICI QUE VOUS MODIFIEZ LE NOM DU BUSINESS!**

Ajoutez une nouvelle cellule et **copiez-collez ce code**:

```python
from google_scraper import GoogleBusinessScraper

# ⚙️ CONFIGURATION - MODIFIEZ ICI
BUSINESS_NAME = "Café Olimpico Montreal"  # ← Changez le nom ici!
MAX_REVIEWS = 30  # ← Nombre de reviews à récupérer

print("="*60)
print("🚀 GOOGLE BUSINESS REVIEWS SCRAPER")
print("="*60)

# Créer le scraper
scraper = GoogleBusinessScraper()

try:
    # Récupérer les reviews
    reviews = scraper.scrape_reviews(BUSINESS_NAME, MAX_REVIEWS)

    if reviews:
        # Exporter en CSV
        scraper.export_to_csv(reviews, "google_reviews.csv")

        # Afficher un résumé
        print("\n" + "="*60)
        print("📈 RÉSUMÉ")
        print("="*60)

        sentiments = {}
        for r in reviews:
            sentiments[r['sentiment']] = sentiments.get(r['sentiment'], 0) + 1

        print(f"\nRépartition des sentiments:")
        for sentiment, count in sorted(sentiments.items()):
            percentage = (count / len(reviews)) * 100
            bar = "█" * int(percentage / 5)
            print(f"  {sentiment:15} {bar} {count} ({percentage:.1f}%)")

        # Télécharger le fichier CSV
        print("\n📥 Téléchargement du fichier CSV...")
        from google.colab import files
        files.download('google_reviews.csv')
        print("✅ Fichier téléchargé! Vérifiez vos téléchargements.")

    else:
        print("\n❌ Aucune review trouvée.")
        print("💡 Vérifiez le nom du business et réessayez.")

except Exception as e:
    print(f"\n❌ Erreur: {e}")
    print("\n💡 Conseils:")
    print("   - Vérifiez le nom du business")
    print("   - Assurez-vous que le business existe sur Google Maps")
    print("   - Réexécutez la cellule")

finally:
    scraper.close()
    print("\n👋 Terminé!")
```

**AVANT DE CLIQUER SUR PLAY**:
- Changez `"Café Olimpico Montreal"` par le nom du business que vous voulez analyser
- Changez `30` si vous voulez plus ou moins de reviews

Puis cliquez sur **Play** (▶).

---

## 📥 Étape 6: Récupérer votre fichier CSV

Après quelques secondes (1-2 minutes), un fichier `google_reviews.csv` va se télécharger automatiquement dans votre dossier Téléchargements!

Ouvrez-le avec Excel, Google Sheets ou n'importe quel logiciel de tableur.

---

## 🎉 C'est terminé!

Vous avez maintenant un fichier CSV avec:
- Les noms des auteurs
- Les notes (étoiles)
- Les dates
- Les commentaires complets
- Les scores de sentiment
- Les labels de sentiment

---

## ⚠️ Si ça ne marche pas

### Problème: "Aucune review trouvée"

**Solutions**:
1. Vérifiez que le nom du business est correct
2. Essayez avec le nom + la ville (ex: "Restaurant ABC Montreal")
3. Essayez avec l'adresse complète
4. Vérifiez que le business existe sur Google Maps

### Problème: "Erreur lors de l'installation"

**Solution**: Réexécutez la cellule 1 (installation)

### Problème: Le téléchargement ne démarre pas

**Solution**:
1. Cliquez sur l'icône 📁 (Fichiers) dans la barre latérale gauche de Colab
2. Trouvez `google_reviews.csv`
3. Faites un clic droit → Télécharger

---

## 🔄 Pour analyser un autre business

Vous n'avez PAS besoin de tout refaire!

**Juste**:
1. Modifiez le nom dans la **Cellule 4**
2. Cliquez sur **Play** (▶) dans la Cellule 4

---

## 📌 Astuces

- **Reviews en français**: Le scraper détecte et analyse les sentiments en français!
- **Plus de reviews**: Changez `MAX_REVIEWS = 30` à `MAX_REVIEWS = 100` (mais ça prend plus de temps)
- **Garder le notebook**: Sauvegardez le notebook Colab (Fichier → Enregistrer) pour le réutiliser plus tard

---

## 🆘 Besoin d'aide?

Si vous êtes bloqué, contactez-moi et décrivez:
1. À quelle étape vous êtes bloqué
2. Le message d'erreur (si il y en a un)
3. Le nom du business que vous essayez d'analyser

Bonne chance! 🍀
