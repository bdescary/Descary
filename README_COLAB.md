# 🎯 Démarrage Rapide - Google Colab

Vous voulez récupérer des reviews Google Business rapidement et gratuitement? Suivez ce guide!

## 🚀 Version Ultra-Rapide (1 étape)

### Option 1: Tout-en-un (PLUS SIMPLE)

1. Allez sur **https://colab.research.google.com**
2. Créez un nouveau notebook
3. Ouvrez le fichier **`COLAB_TOUT_EN_UN.py`** de ce projet
4. **Copiez TOUT le contenu** du fichier
5. **Collez** dans la cellule Colab
6. Modifiez ces 2 lignes:
   ```python
   BUSINESS_NAME = "Café Olimpico Montreal"  # ← Votre business ici
   MAX_REVIEWS = 30  # ← Nombre de reviews
   ```
7. Cliquez sur **Play** ▶
8. Attendez 2-3 minutes
9. Le fichier CSV se télécharge automatiquement! 🎉

**C'est tout!** Vous avez un fichier CSV avec toutes les reviews.

---

## 📚 Version Détaillée (4 étapes)

Si vous préférez comprendre chaque étape, consultez le fichier **`GUIDE_COLAB_SIMPLE.md`**

Ce guide vous explique:
- Comment installer les dépendances
- Comment créer l'analyseur de sentiment
- Comment créer le scraper
- Comment utiliser le scraper
- Comment résoudre les problèmes courants

---

## 📥 Que contient le fichier CSV?

| Colonne | Exemple |
|---------|---------|
| **id** | 1 |
| **auteur** | Marie Dupont |
| **note** | 5 |
| **date** | Il y a 2 mois |
| **commentaire** | Excellent restaurant, je recommande! |
| **sentiment_score** | 0.856 |
| **sentiment** | Très Positif |

---

## ❓ Questions fréquentes

### Combien de temps ça prend?
- Installation: 30-60 secondes
- Scraping: 1-2 minutes pour 30 reviews
- Total: ~3 minutes

### C'est vraiment gratuit?
Oui! Google Colab est 100% gratuit.

### Je peux analyser plusieurs businesses?
Oui! Il suffit de:
1. Changer le nom du business dans le code
2. Réexécuter la cellule

### Ça marche en français?
Oui! L'analyse de sentiment détecte les mots français et anglais.

### Combien de reviews je peux récupérer?
- Recommandé: 30-50 reviews
- Maximum: ~100 reviews (dépend du business)
- Plus vous en demandez, plus ça prend de temps

### Ça ne trouve pas mon business?
Essayez:
- Nom complet + ville: `"Restaurant ABC Montreal"`
- Avec l'adresse: `"Restaurant ABC 123 Rue Principale Montreal"`
- Vérifiez que le business existe sur Google Maps

---

## 📖 Fichiers d'aide disponibles

| Fichier | Description |
|---------|-------------|
| **COLAB_TOUT_EN_UN.py** | ⭐ Code complet à copier-coller (RECOMMANDÉ) |
| **GUIDE_COLAB_SIMPLE.md** | Guide détaillé étape par étape |
| **INSTALLATION_CLOUD.md** | Comparatif des plateformes cloud |

---

## 🆘 Besoin d'aide?

1. Lisez le **GUIDE_COLAB_SIMPLE.md** pour les instructions détaillées
2. Consultez la section "Si ça ne marche pas" dans le guide
3. Vérifiez que le business existe sur Google Maps

---

## ✅ Prochaines étapes

Une fois que vous avez votre fichier CSV:

1. **Ouvrez-le avec Excel ou Google Sheets**
2. **Analysez les données**:
   - Filtrez par note (5 étoiles, 1 étoile, etc.)
   - Filtrez par sentiment (Très Positif, Négatif, etc.)
   - Créez des graphiques
3. **Identifiez les tendances**:
   - Qu'est-ce qui revient dans les reviews positives?
   - Quelles sont les plaintes récurrentes?
   - Comment améliorer votre business?

---

**Bon scraping! 🚀**
