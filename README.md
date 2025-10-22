# Calculateur de Taux d'Absentéisme

Calculateur de taux d'absentéisme pour entreprises françaises, conforme aux normes du droit du travail français.

## 🆕 Version 3.0 disponible !

**Design ultra-moderne** avec animations dynamiques et interface repensée. [Voir le guide V3](GUIDE-V3.md)

## ✨ Fonctionnalités

- **Calcul automatique** du taux d'absentéisme selon la formule standard française
- **Comparaison sectorielle** : comparez votre taux avec la moyenne nationale de votre secteur (12 secteurs disponibles)
- **Périodes flexibles** : mensuel, trimestriel, annuel ou personnalisé
- **Deux modes de saisie** : en heures ou en jours
- **Analyse détaillée** par type d'absence (maladie, accident du travail, congés sans solde, etc.)
- **Interprétation automatique** des résultats avec indicateurs visuels
- **Barre de progression** montrant votre position par rapport à votre secteur
- **Interface responsive** adaptée aux mobiles et tablettes
- **Compatible WordPress/Elementor** : version tout-en-un prête à l'emploi
- **🆕 V3 : Design moderne** avec animations fluides et effets glassmorphism
- **🆕 V3 : Palette de couleurs 2024-2025** (Indigo & Rose)
- **🆕 V3 : Police Inter** pour un rendu professionnel
- **🆕 V3 : Micro-animations** et feedback visuel avancé

## Formule de calcul

```
Taux d'absentéisme = (Nombre d'heures d'absence / Nombre d'heures théoriques travaillées) × 100
```

## 🏢 Secteurs d'activité (Moyennes nationales françaises)

| Secteur | Taux moyen |
|---------|------------|
| BTP / Construction | 7.5% |
| Industrie / Production | 5.5% |
| Commerce / Distribution | 4.5% |
| Services aux entreprises | 3.5% |
| Santé / Social | 6.5% |
| Transport / Logistique | 8.5% |
| Hôtellerie / Restauration | 6.8% |
| Fonction publique | 7.8% |
| Finance / Assurance | 3.2% |
| Agriculture | 5.3% |
| Éducation / Formation | 6.2% |
| Moyenne nationale | 5.0% |

## Types d'absences pris en compte

- Maladie ordinaire
- Accident du travail / Maladie professionnelle
- Congés sans solde
- Absences injustifiées
- Autres absences

**Note** : Les congés payés légaux ne sont généralement pas comptabilisés dans le calcul de l'absentéisme.

## Interprétation des résultats

| Taux | Interprétation |
|------|----------------|
| < 3% | Excellent - Très bas, bonne santé organisationnelle |
| 3-5% | Bon - Dans la moyenne française |
| 5-8% | À surveiller - Légèrement élevé |
| > 8% | Préoccupant - Actions correctives recommandées |

## 🚀 Utilisation

### Version 3.0 - Ultra-Moderne (Recommandée) ⭐

**Design 2024-2025** avec animations dynamiques !

1. Ouvrez `calculateur-absenteisme-v3.html`
2. Copiez TOUT le contenu (Ctrl+A puis Ctrl+C)
3. Dans Elementor, ajoutez un widget **HTML**
4. Collez le contenu et publiez !

📖 **Guide complet V3** : [GUIDE-V3.md](GUIDE-V3.md)

### Version 2.0 - Moderne

Version sobre avec comparaison sectorielle.

1. Ouvrez `calculateur-absenteisme-elementor.html`
2. Copiez et collez dans Elementor
3. Publiez !

📖 **Guide V2** : [GUIDE-ELEMENTOR.md](GUIDE-ELEMENTOR.md)

### Version 1.0 - Classique (Standalone)

Version HTML simple pour navigateur.

1. Ouvrez `calculateur-absenteisme.html` dans votre navigateur
2. Remplissez le formulaire
3. Calculez !

### Méthodes avancées WordPress

- Via plugin : voir `/wordpress-elementor/`
- Installation modulaire : voir `/wordpress-elementor/README-INSTALLATION.md`

## Contexte français

Le calculateur est adapté au contexte français avec :
- Durée légale du travail : 35 heures par semaine
- Terminologie conforme au droit du travail français
- Référence aux normes et moyennes nationales

## Technologies

- HTML5
- CSS3 (avec design moderne et responsive)
- JavaScript vanilla (aucune dépendance externe)
- Compatible WordPress & Elementor Pro

## 📁 Structure du projet

```
Descary/
├── calculateur-absenteisme-v3.html           # ⭐ V3.0 Design ultra-moderne (NOUVEAU)
├── calculateur-absenteisme-elementor.html    # V2.0 Version Elementor
├── calculateur-absenteisme.html              # V1.0 Version standalone
├── GUIDE-V3.md                               # 🆕 Guide version 3.0
├── GUIDE-ELEMENTOR.md                        # Guide version 2.0
├── wordpress-elementor/                      # Version WordPress avancée
│   ├── calculateur-absenteisme.css
│   ├── calculateur-absenteisme.js
│   ├── calculateur-absenteisme-html.html
│   ├── calculateur-absenteisme-shortcode.php
│   └── README-INSTALLATION.md
└── README.md                                 # Ce fichier
```

## 🎨 Quelle version choisir ?

| Version | Design | Animations | Recommandé pour |
|---------|--------|------------|-----------------|
| **V3.0** 🏆 | Ultra-moderne | Avancées | Sites modernes, effet WOW |
| V2.0 | Moderne | Basiques | Bon compromis |
| V1.0 | Classique | Aucune | Maximum de compatibilité |

## Compatibilité

Compatible avec tous les navigateurs modernes :
- Chrome/Edge (version récente)
- Firefox (version récente)
- Safari (version récente)

## Licence

Projet open source - Libre d'utilisation

---

**Taux moyen d'absentéisme en France** : environ 4-5% selon les études récentes
