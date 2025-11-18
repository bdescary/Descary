# Extracteur d'Avis Google Business Profile

Application web pour récupérer, analyser et exporter les avis d'une fiche Google Business Profile.

## 🌟 Fonctionnalités

- **Récupération des avis** : Collecte les commentaires, notes et informations des avis Google Business
- **Analyse de sentiment** : Analyse automatique du sentiment (positif, négatif, neutre) de chaque commentaire
- **Statistiques détaillées** : Affichage de la note moyenne, nombre d'avis total, répartition des sentiments
- **Export CSV** : Exportation des données en format CSV pour analyse ultérieure
- **Interface intuitive** : Design moderne et responsive

## 📋 Utilisation

### Méthode 1 : Données de démonstration (recommandé pour tester)

1. Ouvrez `google-reviews-scraper.html` dans votre navigateur
2. Cliquez sur "Charger données démo"
3. Les avis de démonstration s'afficheront automatiquement
4. Utilisez le bouton "Exporter en CSV" pour télécharger les données

### Méthode 2 : Import de fichier JSON

1. Préparez un fichier JSON avec la structure suivante :
```json
[
  {
    "author": "Nom de l'auteur",
    "rating": 5,
    "text": "Commentaire de l'avis",
    "date": "2024-11-18"
  }
]
```
2. Cliquez sur "Choisir un fichier" et sélectionnez votre JSON
3. Les avis s'afficheront automatiquement

### Méthode 3 : API Google Places (nécessite configuration)

⚠️ **Important** : L'utilisation directe de l'API Google Places depuis le navigateur est bloquée par CORS. Vous devez utiliser un serveur backend.

#### Configuration requise :

1. **Obtenir une clé API Google Places** :
   - Allez sur [Google Cloud Console](https://console.cloud.google.com/)
   - Créez un nouveau projet ou sélectionnez un projet existant
   - Activez l'API "Places API"
   - Créez des identifiants (clé API)
   - Configurez les restrictions de la clé

2. **Configurer un serveur backend** (voir section Backend ci-dessous)

3. **Obtenir un Place ID** :
   - Utilisez [Place ID Finder](https://developers.google.com/maps/documentation/places/web-service/place-id)
   - Ou cherchez votre établissement sur Google Maps et récupérez l'ID dans l'URL

## 🔧 Configuration Backend (Optionnel)

Pour utiliser l'API Google Places, vous devez créer un serveur backend pour éviter les problèmes CORS.

### Exemple avec Node.js :

Créez un fichier `server.js` :

```javascript
const express = require('express');
const cors = require('cors');
const axios = require('axios');
require('dotenv').config();

const app = express();
app.use(cors());
app.use(express.json());

const GOOGLE_API_KEY = process.env.GOOGLE_API_KEY;

app.get('/api/reviews/:placeId', async (req, res) => {
  try {
    const { placeId } = req.params;
    const url = `https://maps.googleapis.com/maps/api/place/details/json`;

    const response = await axios.get(url, {
      params: {
        place_id: placeId,
        fields: 'reviews,rating,user_ratings_total,name',
        key: GOOGLE_API_KEY
      }
    });

    res.json(response.data);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
```

Installation des dépendances :
```bash
npm init -y
npm install express cors axios dotenv
```

Créez un fichier `.env` :
```
GOOGLE_API_KEY=votre_cle_api_ici
```

Lancez le serveur :
```bash
node server.js
```

## 📊 Format d'Export CSV

Le fichier CSV exporté contient les colonnes suivantes :
- **Auteur** : Nom de l'auteur de l'avis
- **Note** : Note attribuée (1 à 5 étoiles)
- **Commentaire** : Texte du commentaire
- **Sentiment** : Analyse du sentiment (Positif, Négatif, Neutre)
- **Date** : Date de l'avis

## 🎨 Fonctionnalités de l'Analyse de Sentiment

L'application analyse automatiquement le sentiment de chaque commentaire en utilisant :
- Une liste de mots-clés positifs (excellent, super, génial, etc.)
- Une liste de mots-clés négatifs (mauvais, horrible, décevant, etc.)
- Un algorithme de comptage pour déterminer le sentiment global

## 🌐 Compatibilité

- ✅ Chrome, Firefox, Safari, Edge (versions récentes)
- ✅ Responsive : fonctionne sur desktop, tablette et mobile
- ✅ Pas de dépendances externes nécessaires pour la version de base

## 📝 Notes Importantes

1. **Limitations de l'API Google Places** :
   - Maximum 5 avis retournés par défaut
   - Nécessite une clé API valide
   - Soumis aux quotas et limites de Google

2. **Données de démonstration** :
   - Idéal pour tester l'application
   - Contient des exemples variés d'avis

3. **Sécurité** :
   - Ne jamais exposer votre clé API dans le code frontend
   - Toujours utiliser un backend pour les appels API
   - Configurer des restrictions sur votre clé API

## 🚀 Améliorations Futures

- [ ] Support de l'authentification Google OAuth
- [ ] Récupération de plus de 5 avis via pagination
- [ ] Graphiques et visualisations avancées
- [ ] Export en format Excel (.xlsx)
- [ ] Analyse de sentiment plus sophistiquée avec IA
- [ ] Comparaison avec les concurrents
- [ ] Notifications pour nouveaux avis

## 📄 Licence

Ce projet est libre d'utilisation pour des fins personnelles et commerciales.

## 🤝 Support

Pour toute question ou problème, veuillez créer une issue sur le dépôt GitHub.
