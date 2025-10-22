# Calculateur de Taux d'Absentéisme

Calculateur de taux d'absentéisme pour entreprises françaises, conforme aux normes du droit du travail français.

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

## Utilisation

### Version Standalone (HTML)

1. Ouvrez le fichier `calculateur-absenteisme.html` dans votre navigateur web
2. Sélectionnez la période d'analyse (mensuel, trimestriel, annuel ou personnalisé)
3. Renseignez :
   - Le nombre de salariés
   - Les heures hebdomadaires par salarié (35h par défaut)
   - Le total des absences (en heures ou en jours)
4. Optionnel : Activez le détail par type d'absence pour une analyse approfondie
5. Cliquez sur "Calculer le taux d'absentéisme"

### Version WordPress/Elementor (Recommandée)

**🎯 Version tout-en-un** : Un seul fichier à copier-coller !

1. Ouvrez `calculateur-absenteisme-elementor.html`
2. Copiez TOUT le contenu (Ctrl+A puis Ctrl+C)
3. Dans Elementor, ajoutez un widget **HTML**
4. Collez le contenu
5. Publiez !

📖 **Guide détaillé** : Consultez `GUIDE-ELEMENTOR.md`

**Autres méthodes (avancées)** :
- Via plugin WordPress : voir `/wordpress-elementor/`
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

## Structure du projet

```
Descary/
├── calculateur-absenteisme.html              # Version standalone (navigateur)
├── calculateur-absenteisme-elementor.html    # ⭐ Version Elementor tout-en-un
├── GUIDE-ELEMENTOR.md                        # Guide d'installation Elementor
├── wordpress-elementor/                      # Version WordPress/Elementor (avancée)
│   ├── calculateur-absenteisme.css
│   ├── calculateur-absenteisme.js
│   ├── calculateur-absenteisme-html.html
│   ├── calculateur-absenteisme-shortcode.php
│   └── README-INSTALLATION.md               # Guide d'installation détaillé
└── README.md                                 # Ce fichier
```

## Compatibilité

Compatible avec tous les navigateurs modernes :
- Chrome/Edge (version récente)
- Firefox (version récente)
- Safari (version récente)

## Licence

Projet open source - Libre d'utilisation

---

**Taux moyen d'absentéisme en France** : environ 4-5% selon les études récentes
