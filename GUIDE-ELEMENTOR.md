# Guide d'Installation Elementor - Calculateur d'Absentéisme

## 📋 Version Tout-en-un pour Elementor Pro

Ce fichier contient **TOUT** en un seul fichier HTML : CSS + HTML + JavaScript

## 🚀 Installation en 3 étapes

### Étape 1 : Ouvrir le fichier source

1. Ouvrez le fichier `calculateur-absenteisme-elementor.html` avec un éditeur de texte
2. Sélectionnez **TOUT le contenu** (Ctrl+A ou Cmd+A)
3. Copiez le contenu (Ctrl+C ou Cmd+C)

### Étape 2 : Créer votre page dans Elementor

1. Connectez-vous à votre WordPress
2. Allez dans **Pages → Ajouter** ou éditez une page existante
3. Cliquez sur **Modifier avec Elementor**

### Étape 3 : Ajouter le widget HTML

1. Dans l'éditeur Elementor, glissez-déposez le widget **HTML** dans votre page
2. Collez tout le contenu copié à l'étape 1
3. Cliquez sur **Mettre à jour** ou **Publier**

**C'est terminé !** 🎉

---

## ✨ Nouvelles Fonctionnalités

### 🏢 Comparaison Sectorielle

Le calculateur inclut maintenant une comparaison avec les moyennes nationales françaises par secteur :

- **BTP / Construction** : 7.5%
- **Industrie / Production** : 5.5%
- **Commerce / Distribution** : 4.5%
- **Services aux entreprises** : 3.5%
- **Santé / Social** : 6.5%
- **Transport / Logistique** : 8.5%
- **Hôtellerie / Restauration** : 6.8%
- **Fonction publique** : 7.8%
- **Finance / Assurance** : 3.2%
- **Agriculture** : 5.3%
- **Éducation / Formation** : 6.2%
- **Autre secteur** : 5.0% (moyenne nationale)

### 📊 Visualisation

- Barre de progression visuelle comparant votre taux au secteur
- Écart calculé automatiquement (+/- X%)
- Interprétation contextuelle selon votre secteur
- Code couleur : vert si en dessous de la moyenne, orange si au-dessus

---

## 🎨 Personnalisation

### Modifier les couleurs du dégradé

Recherchez dans le code :
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

Remplacez par vos couleurs :
```css
background: linear-gradient(135deg, #VOTRE_COULEUR1 0%, #VOTRE_COULEUR2 100%);
```

### Modifier les moyennes sectorielles

Recherchez dans le JavaScript :
```javascript
const sectorAverages = {
    'construction': { avg: 7.5, name: 'BTP / Construction' },
    // ...
```

Modifiez les valeurs `avg:` selon vos données.

### Ajouter un nouveau secteur

Ajoutez une option dans le HTML :
```html
<option value="nouveau_secteur">Nom du nouveau secteur</option>
```

Puis ajoutez la moyenne dans le JavaScript :
```javascript
'nouveau_secteur': { avg: 5.0, name: 'Nom du nouveau secteur' },
```

---

## 📱 Design Responsive

Le calculateur s'adapte automatiquement :

- **Desktop (≥ 1024px)** : Layout 2 colonnes
  - Gauche : Formulaire
  - Droite : Résultats (sticky, reste visible au scroll)

- **Tablette (768-1023px)** : Layout 1 colonne optimisé

- **Mobile (< 768px)** : Layout compact avec scroll vers les résultats

---

## 🔧 Compatibilité

- ✅ WordPress 5.0+
- ✅ Elementor (gratuit)
- ✅ Elementor Pro
- ✅ Tous navigateurs modernes (Chrome, Firefox, Safari, Edge)
- ✅ Compatible avec tous les thèmes WordPress

---

## 🐛 Dépannage

### Le calculateur ne s'affiche pas

- Vérifiez que vous avez copié **TOUT** le contenu du fichier
- Assurez-vous d'utiliser le widget **HTML** (pas Texte)
- Videz le cache de votre navigateur et WordPress

### Le design est cassé

- Le thème peut avoir des styles qui entrent en conflit
- Ajoutez `!important` aux styles si nécessaire
- Vérifiez que le widget HTML a assez d'espace (section pleine largeur recommandée)

### Le JavaScript ne fonctionne pas

- Vérifiez la console du navigateur (F12)
- Assurez-vous qu'aucun autre plugin ne bloque le JavaScript
- Testez en désactivant temporairement les autres plugins

### Les calculs sont incorrects

- Vérifiez que vous avez saisi des nombres valides
- Le mode heures/jours doit être correctement sélectionné
- Pour le détail par type, la somme doit correspondre au total

---

## 💡 Conseils d'Utilisation

### Placement recommandé

1. Créez une section **pleine largeur** dans Elementor
2. Ajoutez le widget HTML dans cette section
3. Désactivez les padding de la section si besoin

### Pour une meilleure intégration

- Placez le calculateur dans une page dédiée
- Ou utilisez une popup Elementor Pro
- Ou intégrez dans un onglet (widget Tabs)

### Optimisation SEO

Ajoutez du contenu texte autour du calculateur :
- Explication de l'absentéisme
- Importance pour les RH
- Liens vers ressources légales

---

## 📊 Données Sectorielles

Les moyennes nationales sont basées sur les études françaises récentes (2023-2024) :

**Sources** :
- Baromètre de l'absentéisme Ayming-AG2R
- Études DARES (Ministère du Travail)
- Données CNAMTS

**Note** : Ces moyennes sont indicatives et peuvent varier selon :
- La taille de l'entreprise
- La région géographique
- Les conditions de travail
- La période de l'année

---

## 🔄 Mise à jour

Pour mettre à jour le calculateur :

1. Sauvegardez votre version actuelle (copier le contenu du widget)
2. Téléchargez la nouvelle version
3. Remplacez le contenu du widget HTML
4. Testez le fonctionnement
5. Videz le cache

---

## 📞 Support

Pour toute question :
- Consultez d'abord ce guide
- Vérifiez la console du navigateur pour les erreurs
- Ouvrez une issue sur GitHub : https://github.com/bdescary/Descary/issues

---

## 📄 Licence

Open source - Libre d'utilisation et de modification

**Version** : 2.0
**Dernière mise à jour** : 2025-10-22
**Nouveautés** : Comparaison sectorielle + version tout-en-un
