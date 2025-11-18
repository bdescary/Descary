# 🌟 Google Business Reviews Scraper

Application Python pour récupérer automatiquement les commentaires, notes et sentiments d'une fiche Google Business Profile, avec export en CSV.

## 📋 Fonctionnalités

- ✅ Récupération automatique des reviews Google Business Profile
- ⭐ Extraction des notes (nombre d'étoiles)
- 💬 Extraction des commentaires complets
- 😊 Analyse de sentiment automatique (français et anglais)
- 📅 Récupération des dates de publication
- 👤 Extraction des noms des auteurs
- 📊 Export en CSV
- 📈 Statistiques et résumé des reviews

## 🔧 Prérequis

- Python 3.8 ou supérieur
- Chrome ou Chromium installé sur votre système
- Connexion internet

## 📦 Installation

### 1. Cloner le projet

```bash
git clone <url-du-repo>
cd Descary
```

### 2. Créer un environnement virtuel (recommandé)

```bash
# Créer l'environnement virtuel
python3 -m venv venv

# Activer l'environnement virtuel
# Sur Linux/Mac:
source venv/bin/activate

# Sur Windows:
venv\Scripts\activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

Cette commande installera automatiquement:
- Selenium (pour l'automatisation du navigateur)
- BeautifulSoup4 (pour le parsing HTML)
- VADER Sentiment (pour l'analyse de sentiment)
- TextBlob (pour la détection de langue)
- Pandas (pour la manipulation de données)
- WebDriver Manager (pour gérer ChromeDriver automatiquement)

## 🚀 Utilisation

### Mode interactif (recommandé pour débuter)

Lancez simplement le script principal:

```bash
python google_business_scraper.py
```

Le programme vous demandera:
1. Le nom et l'adresse du business (ex: "Restaurant Le Gourmet Montreal")
2. Le nombre maximum de reviews à récupérer (ex: 50)

### Mode programmation

Vous pouvez aussi utiliser le scraper dans votre propre code Python:

```python
from google_business_scraper import GoogleBusinessScraper

# Créer une instance du scraper
scraper = GoogleBusinessScraper(headless=True)

try:
    # Option 1: Recherche par nom et adresse
    reviews = scraper.scrape_reviews(
        search_query="Restaurant Le Gourmet Montreal",
        max_reviews=100
    )

    # Option 2: Recherche par Place ID (si vous l'avez)
    reviews = scraper.scrape_reviews(
        place_id="ChIJN1t_tDeuEmsRUsoyG83frY4",
        max_reviews=100
    )

    # Exporter en CSV
    filename = scraper.export_to_csv(reviews, filename="mes_reviews.csv")

    print(f"✅ {len(reviews)} reviews exportées dans {filename}")

finally:
    scraper.close()
```

## 📁 Structure des données exportées

Le fichier CSV contient les colonnes suivantes:

| Colonne | Description | Exemple |
|---------|-------------|---------|
| `id` | Numéro séquentiel de la review | 1, 2, 3... |
| `auteur` | Nom de l'auteur | "Marie Dupont" |
| `note` | Note sur 5 étoiles | 5 |
| `date` | Date de publication | "Il y a 2 mois" |
| `commentaire` | Texte complet du commentaire | "Excellent restaurant..." |
| `sentiment_score` | Score de sentiment (-1 à 1) | 0.856 |
| `sentiment` | Label de sentiment | "Très Positif" |

### Labels de sentiment

- **Très Positif**: Score ≥ 0.5
- **Positif**: Score entre 0.1 et 0.5
- **Neutre**: Score entre -0.1 et 0.1
- **Négatif**: Score entre -0.5 et -0.1
- **Très Négatif**: Score < -0.5

## 🎯 Exemples d'utilisation

### Exemple 1: Analyser un restaurant local

```bash
python google_business_scraper.py
# Entrez: "Café Olimpico Montreal"
# Nombre de reviews: 50
```

### Exemple 2: Tester l'analyseur de sentiment

```bash
python sentiment_analyzer.py
```

Ce script de test affichera des exemples d'analyse de sentiment en français et en anglais.

### Exemple 3: Script personnalisé

```python
from google_business_scraper import GoogleBusinessScraper
import pandas as pd

scraper = GoogleBusinessScraper(headless=False)

try:
    # Récupérer les reviews
    reviews = scraper.scrape_reviews(
        search_query="Schwartz's Deli Montreal",
        max_reviews=200
    )

    # Convertir en DataFrame pandas pour analyse
    df = pd.DataFrame(reviews)

    # Filtrer uniquement les reviews positives
    positive_reviews = df[df['sentiment_score'] > 0.5]

    # Sauvegarder séparément
    scraper.export_to_csv(positive_reviews.to_dict('records'),
                          filename="reviews_positives.csv")

    # Afficher des statistiques
    print(f"Note moyenne: {df['note'].mean():.2f}")
    print(f"Sentiment moyen: {df['sentiment_score'].mean():.3f}")

finally:
    scraper.close()
```

## ⚙️ Configuration

### Mode headless

Par défaut, le navigateur s'exécute en arrière-plan. Pour voir le navigateur en action:

```python
scraper = GoogleBusinessScraper(headless=False)
```

### Nombre de reviews

Le paramètre `max_reviews` contrôle le nombre maximum de reviews à récupérer. Note: Google Maps peut limiter le nombre de reviews affichées.

### Temps d'attente

Vous pouvez ajuster les temps d'attente dans le code si vous avez une connexion lente:

```python
# Dans google_business_scraper.py, ligne ~140
time.sleep(3)  # Augmenter cette valeur si nécessaire
```

## 🐛 Résolution de problèmes

### Erreur: ChromeDriver non trouvé

Le script utilise `webdriver-manager` qui télécharge automatiquement ChromeDriver. Si vous rencontrez des problèmes:

```bash
pip install --upgrade webdriver-manager
```

### Erreur: Aucune review trouvée

1. Vérifiez que le nom du business est correct
2. Essayez avec `headless=False` pour voir ce qui se passe
3. Augmentez les temps d'attente (`time.sleep()`)
4. Le business a peut-être très peu de reviews

### Erreur: Timeout

Si la page met trop de temps à charger:

1. Vérifiez votre connexion internet
2. Augmentez le timeout dans le code
3. Essayez avec moins de reviews

### Les sentiments semblent incorrects

L'analyse de sentiment fonctionne mieux avec:
- Des textes en français ou en anglais
- Des commentaires complets (pas juste "Bien" ou "Nul")
- Des phrases structurées

Pour des langues autres que FR/EN, vous devrez adapter le module `sentiment_analyzer.py`.

## 📝 Notes importantes

### Limitations

- **Limite de reviews**: Google Maps peut ne pas afficher toutes les reviews d'un business
- **Vitesse**: Le scraping prend du temps (environ 1-2 secondes par review)
- **Stabilité**: Les sélecteurs CSS peuvent changer si Google modifie son interface
- **Rate limiting**: Évitez de faire trop de requêtes rapidement

### Considérations éthiques et légales

- ⚖️ Utilisez cet outil de manière responsable
- 📜 Respectez les conditions d'utilisation de Google
- 🔒 Ne collectez que les données publiques
- 🎯 Utilisez les données pour des analyses légitimes
- ⏱️ N'abusez pas en faisant trop de requêtes

### Bonnes pratiques

1. **Testez d'abord avec peu de reviews** (ex: 10-20)
2. **Utilisez headless=False** lors du débogage
3. **Sauvegardez régulièrement** vos exports CSV
4. **Attendez entre les requêtes** si vous scrapez plusieurs businesses
5. **Vérifiez la qualité** des données exportées

## 🔄 Mises à jour futures possibles

- [ ] Support pour l'API officielle Google My Business
- [ ] Export en JSON et Excel
- [ ] Interface graphique (GUI)
- [ ] Analyse de sentiment multilingue améliorée
- [ ] Graphiques et visualisations
- [ ] Détection de spam/fake reviews
- [ ] Comparaison entre plusieurs businesses
- [ ] Suivi temporel des reviews

## 📞 Support

En cas de problème:
1. Vérifiez que toutes les dépendances sont installées
2. Consultez la section "Résolution de problèmes"
3. Vérifiez que Chrome est bien installé
4. Essayez avec `headless=False` pour voir ce qui se passe

## 📄 Licence

Ce projet est fourni à des fins éducatives et de recherche.

## 🤝 Contribution

Les contributions sont les bienvenues! N'hésitez pas à:
- Signaler des bugs
- Proposer des améliorations
- Ajouter des fonctionnalités

## ✨ Auteur

Créé pour faciliter l'analyse des reviews Google Business Profile.

---

**Bon scraping! 🚀**
