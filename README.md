# Descary - Éditeur Graphique Web

Une application web moderne de conception graphique similaire à Canva, construite avec HTML5 Canvas, CSS3 et JavaScript vanilla.

## 🎨 Fonctionnalités

### Outils de Dessin
- **Formes** : Rectangle, Cercle, Triangle, Ligne
- **Texte** : Ajout et personnalisation de texte avec différentes polices
- **Images** : Import et manipulation d'images
- **Sélection** : Déplacement et modification des éléments

### Manipulation d'Éléments
- ✅ Glisser-déposer (drag & drop)
- ✅ Redimensionnement
- ✅ Rotation (0-360°)
- ✅ Opacité réglable
- ✅ Couleurs personnalisables (remplissage et bordure)
- ✅ Épaisseur de bordure

### Fonctionnalités de Texte
- Polices multiples (Arial, Helvetica, Times New Roman, etc.)
- Taille de police personnalisable
- Styles : Gras, Italique, Souligné
- Texte multiligne

### Gestion des Calques
- Premier plan / Arrière-plan
- Organisation des éléments

### Historique
- ✅ Annuler (Ctrl+Z)
- ✅ Refaire (Ctrl+Y)
- Historique de 50 états

### Export/Import
- **Export PNG** : Téléchargez votre design en image
- **Export JSON** : Sauvegardez votre projet
- **Import JSON** : Rechargez un projet sauvegardé

## 🚀 Utilisation

### Démarrage
1. Ouvrez `index.html` dans votre navigateur web moderne
2. L'application se charge automatiquement

### Créer des Formes
1. Sélectionnez un outil dans la barre latérale gauche
2. Cliquez et faites glisser sur le canvas pour créer la forme
3. Utilisez le panneau de propriétés à droite pour personnaliser

### Ajouter du Texte
1. Cliquez sur l'outil "Texte"
2. Cliquez sur le canvas pour placer le texte
3. Modifiez le contenu et le style dans le panneau de propriétés

### Ajouter des Images
1. Cliquez sur l'outil "Image"
2. Sélectionnez une image depuis votre ordinateur
3. L'image apparaît sur le canvas et peut être déplacée/redimensionnée

### Raccourcis Clavier
- `Suppr` ou `Backspace` : Supprimer l'élément sélectionné
- `Ctrl+Z` : Annuler
- `Ctrl+Y` : Refaire
- `Ctrl+D` : Dupliquer l'élément sélectionné

## 🛠️ Technologies

- **HTML5 Canvas** : Pour le rendu graphique
- **CSS3** : Interface utilisateur moderne et responsive
- **JavaScript (ES6+)** : Logique de l'application
- **Architecture orientée objet** : Classes pour chaque type d'élément

## 📁 Structure du Projet

```
Descary/
├── index.html      # Structure HTML principale
├── style.css       # Styles et interface utilisateur
├── app.js          # Logique de l'application
└── README.md       # Documentation
```

## 🎯 Classes Principales

### CanvasElement
Classe de base pour tous les éléments graphiques.

### Formes Spécifiques
- `Rectangle` : Rectangles avec coins arrondis optionnels
- `Circle` : Cercles et ellipses
- `Triangle` : Triangles
- `Line` : Lignes droites
- `TextElement` : Éléments textuels
- `ImageElement` : Images importées

### CanvasApp
Gestionnaire principal de l'application qui coordonne :
- Rendu du canvas
- Gestion des événements
- Historique (undo/redo)
- Export/Import
- Sélection et manipulation des éléments

## 🌟 Fonctionnalités Avancées

### Système de Propriétés
Chaque élément possède des propriétés modifiables :
- Position (X, Y)
- Dimensions (Largeur, Hauteur)
- Rotation
- Opacité
- Couleurs
- Styles spécifiques au type

### Persistance
Les projets peuvent être sauvegardés au format JSON incluant :
- Tous les éléments et leurs propriétés
- Dimensions du canvas
- Métadonnées du projet

## 📝 Format JSON

```json
{
  "version": "1.0",
  "canvasWidth": 800,
  "canvasHeight": 600,
  "elements": [
    {
      "id": 1234567890,
      "type": "rectangle",
      "x": 100,
      "y": 100,
      "width": 200,
      "height": 150,
      "rotation": 0,
      "opacity": 1,
      "fillColor": "#3b82f6",
      "strokeColor": "#000000",
      "strokeWidth": 2
    }
  ]
}
```

## 🔮 Améliorations Futures

- Groupement d'éléments
- Alignement automatique
- Grille et règles
- Plus de formes prédéfinies
- Filtres et effets d'image
- Collaboration en temps réel
- Templates prédéfinis
- Bibliothèque d'assets

## 📄 Licence

Projet open source - Libre d'utilisation

## 👨‍💻 Développement

Application développée avec des technologies web modernes, sans dépendances externes.
Fonctionne dans tous les navigateurs modernes supportant HTML5 Canvas.

---

**Descary** - Créez, Concevez, Partagez ✨
