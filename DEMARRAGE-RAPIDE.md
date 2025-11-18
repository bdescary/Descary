# 🚀 Guide de Démarrage Rapide

## Utilisation Simple (Sans Installation)

### Option 1 : Données de Démonstration ⭐ RECOMMANDÉ

C'est la méthode la plus simple pour tester l'application immédiatement !

1. **Ouvrir l'application**
   ```
   Ouvrez le fichier google-reviews-scraper.html dans votre navigateur
   (double-cliquez dessus ou faites clic droit > Ouvrir avec > Navigateur)
   ```

2. **Charger les données de test**
   - Cliquez sur le bouton **"Charger données démo"**
   - Les avis de démonstration s'afficheront automatiquement

3. **Explorer les fonctionnalités**
   - Consultez les statistiques (note moyenne, nombre d'avis, sentiments)
   - Parcourez le tableau des avis
   - Cliquez sur **"Exporter en CSV"** pour télécharger les données

✅ **C'est tout ! Aucune installation nécessaire pour cette méthode.**

---

### Option 2 : Importer vos propres données JSON

1. **Préparer votre fichier JSON**

   Utilisez `demo-reviews.json` comme modèle :
   ```json
   [
     {
       "author": "Nom",
       "rating": 5,
       "text": "Commentaire ici",
       "date": "2024-11-18"
     }
   ]
   ```

2. **Importer le fichier**
   - Ouvrez `google-reviews-scraper.html`
   - Section "Ou charger des données de démonstration"
   - Cliquez sur "Choisir un fichier" et sélectionnez votre JSON
   - Les données s'afficheront automatiquement

---

## Utilisation Avancée (Avec Backend)

### Prérequis

- Node.js (version 14 ou supérieure)
- npm (installé avec Node.js)
- Une clé API Google Places

### Installation Rapide

```bash
# 1. Installer les dépendances
npm install

# 2. Configurer la clé API
cp .env.example .env
# Éditez le fichier .env et ajoutez votre GOOGLE_API_KEY

# 3. Lancer le serveur
npm start
```

Le serveur sera accessible à : `http://localhost:3000`

### Utilisation avec le Backend

1. **Ouvrir l'application**
   ```
   http://localhost:3000/google-reviews-scraper.html
   ```

2. **Récupérer les avis**
   - Entrez votre clé API Google Places
   - Entrez le Place ID de l'établissement
   - Cliquez sur "Récupérer les avis"

---

## 📝 Comment Obtenir un Place ID ?

### Méthode 1 : Place ID Finder (Officiel)
1. Allez sur : https://developers.google.com/maps/documentation/places/web-service/place-id
2. Recherchez votre établissement
3. Copiez le Place ID

### Méthode 2 : Google Maps
1. Trouvez votre établissement sur Google Maps
2. Cliquez dessus pour afficher les détails
3. L'URL contient le Place ID après `!1s`
   ```
   Exemple : https://www.google.com/maps/place/...!1sChIJN1t_tDeuEmsRUsoyG83frY4!...
   Place ID : ChIJN1t_tDeuEmsRUsoyG83frY4
   ```

---

## 🔑 Comment Obtenir une Clé API Google Places ?

1. **Créer un compte Google Cloud**
   - Allez sur : https://console.cloud.google.com/

2. **Créer un projet**
   - Cliquez sur "Sélectionner un projet" > "Nouveau projet"
   - Donnez-lui un nom (ex: "Google Reviews Scraper")

3. **Activer l'API Places**
   - Menu "APIs & Services" > "Bibliothèque"
   - Recherchez "Places API"
   - Cliquez sur "Activer"

4. **Créer une clé API**
   - Menu "APIs & Services" > "Identifiants"
   - Cliquez sur "+ CRÉER DES IDENTIFIANTS" > "Clé API"
   - Copiez la clé générée

5. **Sécuriser la clé (Recommandé)**
   - Cliquez sur votre clé pour la modifier
   - Section "Restrictions d'application" : Choisissez "Serveurs HTTP"
   - Ajoutez votre IP ou domaine
   - Section "Restrictions d'API" : Sélectionnez "Places API"
   - Enregistrez

---

## ⚡ Commandes Utiles

```bash
# Installer les dépendances
npm install

# Démarrer le serveur
npm start

# Mode développement (redémarre automatiquement)
npm run dev

# Vérifier l'état du serveur
curl http://localhost:3000/health
```

---

## 🎯 Cas d'Usage

### 1. Test Rapide (2 minutes)
→ Utilisez la méthode "Données de Démonstration"

### 2. Import de Données Existantes (5 minutes)
→ Créez un fichier JSON et importez-le

### 3. Connexion API Google Places (15 minutes)
→ Configurez le backend avec votre clé API

---

## 📊 Format du CSV Exporté

Le fichier CSV contiendra :
- **Auteur** : Nom de l'utilisateur
- **Note** : Note sur 5
- **Commentaire** : Texte complet de l'avis
- **Sentiment** : Positif / Négatif / Neutre
- **Date** : Date de l'avis

Nom du fichier : `avis_google_YYYY-MM-DD.csv`

---

## ❓ Problèmes Fréquents

### Le bouton "Récupérer les avis" ne fonctionne pas
→ Utilisez le backend (voir "Utilisation Avancée") car l'API Google Places ne peut pas être appelée directement depuis le navigateur (problème CORS)

### Les données de démo ne s'affichent pas
→ Vérifiez que JavaScript est activé dans votre navigateur

### Le serveur ne démarre pas
→ Vérifiez que Node.js est installé : `node --version`
→ Vérifiez que le port 3000 n'est pas utilisé

### Erreur "GOOGLE_API_KEY non définie"
→ Créez un fichier `.env` avec votre clé API (voir `.env.example`)

---

## 💡 Conseils

- 🎯 **Pour tester** : Utilisez les données de démo
- 🔐 **Pour la production** : Utilisez le backend avec clé API
- 📊 **Pour analyser** : Exportez en CSV et utilisez Excel/Google Sheets
- 🔄 **Pour automatiser** : Créez un script qui appelle l'API régulièrement

---

## 📞 Support

Si vous rencontrez des problèmes :
1. Vérifiez la section "Problèmes Fréquents" ci-dessus
2. Consultez le fichier README.md pour plus de détails
3. Vérifiez que toutes les dépendances sont installées
4. Consultez les logs du serveur pour les erreurs

---

🎉 **Bon scraping !**
