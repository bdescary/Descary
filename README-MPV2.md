# MPV2 - Calculateur de Taux d'Absentéisme

## 📋 Description

Le **MPV2** est un calculateur moderne et interactif de taux d'absentéisme conçu spécifiquement pour les entreprises françaises. Il permet d'évaluer et d'analyser le taux d'absentéisme en le comparant aux moyennes nationales et sectorielles basées sur des données officielles 2024-2025.

## ✨ Fonctionnalités

- **Calcul précis** du taux d'absentéisme selon la formule standard
- **Comparaison automatique** avec les moyennes nationales, sectorielles et par catégorie socioprofessionnelle
- **9 secteurs d'activité** couverts avec des données actualisées
- **4 catégories socioprofessionnelles** (Cadres, Professions intermédiaires, Employés, Ouvriers)
- **Visualisation interactive** avec graphiques et tableaux
- **Recommandations personnalisées** basées sur les résultats
- **Design responsive** adapté à tous les écrans (mobile, tablette, desktop)
- **Interface moderne** avec animations fluides

## 🎨 Design

Le calculateur adopte une palette de couleurs professionnelle adaptée au secteur médical :

- **Bleu principal** : #0066cc (professionnalisme, confiance)
- **Bleu foncé** : #003d82 (autorité, expertise)
- **Vert accent** : #00a651 (santé, bien-être)
- **Orange accent** : #ff8c00 (avertissements)
- **Rouge accent** : #dc3545 (alertes)

Ces couleurs sont conçues pour s'harmoniser avec l'identité visuelle de Medicat Partner.

## 📊 Sources des données

Les données utilisées proviennent de sources officielles et reconnues pour l'année 2024-2025 :

### Sources principales

1. **Observatoire de l'absentéisme APICIL 2024**
   - Taux moyen national : 4,41%
   - Durée moyenne des arrêts : 21,5 jours
   - URL : https://pro.apicil.com/prevoyance/taux-absenteisme-france/

2. **Baromètre Diot-Siaci 2024-2025**
   - Taux d'absentéisme par secteur détaillés
   - Analyse des tendances 2025
   - URL : https://diot-siaci.com/fr/absenteisme-les-tendances-2025/

3. **Étude WTW (Willis Towers Watson) 2024**
   - Analyse sectorielle approfondie
   - Données historiques et évolutions
   - URL : https://www.wtwco.com/fr-fr/news/2024/09/l-absenteisme-des-salaries-francais-du-secteur-prive-flechit-pour-la-premiere-fois-depuis-2016

4. **Baromètre Ayming & AG2R LA MONDIALE 2024-2025**
   - 17ème édition du Baromètre de l'Absentéisme et de l'Engagement
   - Données par catégorie socioprofessionnelle
   - URL : https://www.ayming.fr/insights/barometres-livres-blancs/barometre-de-labsenteisme-et-de-lengagement/

### Taux d'absentéisme par secteur (2024)

| Secteur | Taux | Source |
|---------|------|--------|
| Santé / Action sociale | 8,30% | Diot-Siaci 2024 |
| Hébergement et restauration | 7,39% | WTW 2024 |
| Commerce | 6,23% | Diot-Siaci 2024 |
| Transport et logistique | 5,40% | Diot-Siaci / WTW 2024 |
| Administration publique | 5,20% | Estimations sectorielles |
| Industrie manufacturière | 4,80% | Moyennes sectorielles |
| Construction | 4,50% | Moyennes sectorielles |
| Services aux entreprises | 3,90% | Moyennes sectorielles |

### Taux d'absentéisme par catégorie socioprofessionnelle (2024)

| Catégorie | Taux | Source |
|-----------|------|--------|
| Ouvriers | 7,77% | Ayming/AG2R 2024 |
| Employés administratifs et agents de service | 6,15% | Ayming/AG2R 2024 |
| Professions intermédiaires | 4,70% | Ayming/AG2R 2024 |
| Cadres | 2,29% | Ayming/AG2R 2024 |

## 🚀 Installation et Utilisation

### Utilisation autonome

Le fichier `mpv2-calculateur-absenteisme.html` est un fichier HTML autonome qui peut être utilisé directement :

```bash
# Ouvrir directement dans un navigateur
open mpv2-calculateur-absenteisme.html
```

### Intégration au site Medicat Partner

#### Option 1 : Page dédiée

Héberger le calculateur comme une page séparée :

```html
<a href="mpv2-calculateur-absenteisme.html" target="_blank">
    Calculateur d'absentéisme
</a>
```

#### Option 2 : Intégration via iframe

Intégrer le calculateur dans une page existante :

```html
<iframe
    src="mpv2-calculateur-absenteisme.html"
    width="100%"
    height="1200px"
    frameborder="0"
    style="border: none;">
</iframe>
```

#### Option 3 : Intégration directe

Pour une intégration complète dans le CMS du site :

1. Copier le contenu de la section `<style>` dans votre fichier CSS
2. Copier le contenu de la section `<body>` dans votre page
3. Copier le contenu de la section `<script>` dans votre fichier JavaScript

## 📱 Compatibilité

- ✅ Chrome, Firefox, Safari, Edge (dernières versions)
- ✅ Mobile iOS et Android
- ✅ Tablettes
- ✅ Responsive design adaptatif

## 🧮 Formule de calcul

Le taux d'absentéisme est calculé selon la formule standard :

```
Taux d'absentéisme (%) = (Nombre de jours d'absence / (Nombre de jours ouvrés × Nombre d'employés)) × 100
```

## 🎯 Interprétation des résultats

Le calculateur fournit une analyse en 4 niveaux :

- **Excellent** (< 3,09%) : Badge vert - Significativement inférieur à la moyenne
- **Bien** (3,09% - 4,41%) : Badge vert - Inférieur à la moyenne nationale
- **À surveiller** (4,41% - 5,73%) : Badge orange - Légèrement supérieur à la moyenne
- **Élevé** (> 5,73%) : Badge rouge - Significativement supérieur à la moyenne

## 🔧 Personnalisation

### Modifier les couleurs

Les couleurs sont définies dans les variables CSS au début du fichier :

```css
:root {
    --primary-blue: #0066cc;
    --dark-blue: #003d82;
    --accent-green: #00a651;
    /* ... autres variables ... */
}
```

### Ajouter des secteurs

Modifier l'objet `sectorData` dans le JavaScript :

```javascript
const sectorData = {
    'nouveau_secteur': { name: 'Nom du secteur', rate: 4.50 },
    // ...
};
```

### Personnaliser les recommandations

Modifier la fonction `getRecommendations()` dans le JavaScript.

## 📄 Licence

© 2025 Medicat Partner - Tous droits réservés

## 📞 Support

Pour toute question ou assistance concernant le calculateur MPV2, contactez l'équipe Medicat Partner.

---

**Version** : 1.0.0
**Date de création** : Novembre 2025
**Dernière mise à jour des données** : 2024-2025
