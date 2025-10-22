# Guide d'Installation - Calculateur d'Absentéisme pour WordPress/Elementor Pro

Ce guide vous explique comment intégrer le calculateur de taux d'absentéisme dans votre site WordPress avec Elementor Pro.

## 📋 Prérequis

- WordPress 5.0 ou supérieur
- Elementor Pro (ou Elementor gratuit pour la méthode 2)
- Accès FTP ou gestionnaire de fichiers WordPress

## 🚀 Méthode 1 : Plugin WordPress avec Shortcode (Recommandé)

### Étape 1 : Installation du Plugin

1. **Créer le dossier du plugin**
   - Accédez à `/wp-content/plugins/`
   - Créez un nouveau dossier : `calculateur-absenteisme`

2. **Télécharger les fichiers**
   - Copiez ces 3 fichiers dans le dossier :
     - `calculateur-absenteisme-shortcode.php`
     - `calculateur-absenteisme.css`
     - `calculateur-absenteisme.js`

3. **Activer le plugin**
   - Allez dans WordPress Admin → Extensions
   - Trouvez "Calculateur de Taux d'Absentéisme"
   - Cliquez sur "Activer"

### Étape 2 : Utilisation avec Elementor

**Option A : Avec le widget Shortcode d'Elementor Pro**

1. Éditez votre page avec Elementor
2. Glissez-déposez le widget **Shortcode** (Elementor Pro)
3. Entrez le shortcode :
   ```
   [calculateur_absenteisme]
   ```
4. Publiez la page

**Option B : Avec le widget HTML**

1. Éditez votre page avec Elementor
2. Glissez-déposez le widget **HTML**
3. Entrez le shortcode :
   ```html
   [calculateur_absenteisme]
   ```
4. Publiez la page

**Option C : Dans l'éditeur classique WordPress**

Ajoutez simplement le shortcode dans votre contenu :
```
[calculateur_absenteisme]
```

### Étape 3 : Personnalisation (optionnel)

Vous pouvez personnaliser le titre et sous-titre :

```
[calculateur_absenteisme titre="Mon Titre Personnalisé" sous_titre="Mon sous-titre"]
```

---

## 🎨 Méthode 2 : Widget HTML Elementor (Sans Plugin)

Cette méthode est idéale si vous ne pouvez pas installer de plugin.

### Étape 1 : Ajouter le CSS

1. Allez dans **WordPress Admin → Apparence → Personnaliser → CSS additionnel**
2. Copiez tout le contenu de `calculateur-absenteisme.css`
3. Collez-le dans le champ CSS additionnel
4. Enregistrez

### Étape 2 : Ajouter le JavaScript

**Option A : Via le thème**

1. Allez dans **Apparence → Éditeur de thème**
2. Ouvrez `functions.php`
3. Ajoutez ce code à la fin :

```php
function enqueue_calculateur_absenteisme_js() {
    wp_enqueue_script('calc-absenteisme', get_stylesheet_directory_uri() . '/js/calculateur-absenteisme.js', array(), '1.0.0', true);
}
add_action('wp_enqueue_scripts', 'enqueue_calculateur_absenteisme_js');
```

4. Créez un dossier `js` dans votre thème
5. Uploadez `calculateur-absenteisme.js` dans ce dossier

**Option B : Via un plugin d'insertion de scripts**

1. Installez un plugin comme "Insert Headers and Footers" ou "WPCode"
2. Copiez le contenu de `calculateur-absenteisme.js`
3. Collez-le dans la section Footer Scripts
4. Enregistrez

### Étape 3 : Ajouter le HTML avec Elementor

1. Éditez votre page avec Elementor
2. Glissez-déposez le widget **HTML**
3. Copiez tout le contenu de `calculateur-absenteisme-html.html`
4. Collez-le dans le widget HTML
5. Publiez la page

---

## 🔧 Méthode 3 : Intégration Manuelle Complète

Pour ceux qui préfèrent tout-en-un dans un seul widget HTML :

1. Créez une nouvelle page dans Elementor
2. Ajoutez un widget **HTML**
3. Copiez-collez ce code complet :

```html
<!-- CSS -->
<style>
[Coller ici le contenu de calculateur-absenteisme.css]
</style>

<!-- HTML -->
[Coller ici le contenu de calculateur-absenteisme-html.html]

<!-- JavaScript -->
<script>
[Coller ici le contenu de calculateur-absenteisme.js]
</script>
```

---

## ✅ Vérification de l'Installation

Après l'installation, vérifiez que :

1. ✓ Le formulaire s'affiche correctement
2. ✓ Les champs de saisie fonctionnent
3. ✓ Le bouton "Calculer" fonctionne
4. ✓ Les résultats s'affichent après le calcul
5. ✓ Le design responsive fonctionne sur mobile

## 🎯 Design Responsive

Le calculateur s'adapte automatiquement :

- **Desktop (≥ 1024px)** : Layout 2 colonnes avec résultats sticky
- **Tablette (768-1023px)** : Layout 1 colonne optimisé
- **Mobile (< 768px)** : Layout mobile compact

## 🐛 Dépannage

### Le calculateur ne s'affiche pas

1. Vérifiez que le CSS est bien chargé
2. Vérifiez la console du navigateur (F12) pour les erreurs JavaScript
3. Assurez-vous qu'il n'y a pas de conflit avec d'autres plugins

### Le JavaScript ne fonctionne pas

1. Vérifiez que jQuery est chargé (WordPress l'inclut par défaut)
2. Vérifiez que le fichier JS est bien uploadé
3. Vérifiez les conflits avec d'autres scripts

### Problèmes de style

1. Vérifiez que le CSS est bien appliqué
2. Les classes CSS utilisent le préfixe `calc-absenteisme-` pour éviter les conflits
3. Ajoutez `!important` si nécessaire pour forcer certains styles

### Conflits avec le thème

Si le design ne s'affiche pas correctement :

1. Augmentez la spécificité CSS en ajoutant `.elementor` devant les classes
2. Utilisez l'éditeur CSS d'Elementor pour surcharger les styles
3. Contactez le support de votre thème pour vérifier la compatibilité

## 🔄 Mise à jour

Pour mettre à jour le calculateur :

1. Remplacez les fichiers CSS et JS par les nouvelles versions
2. Videz le cache WordPress et Elementor
3. Testez le fonctionnement

## 💡 Personnalisation Avancée

### Modifier les couleurs

Éditez le fichier CSS et modifiez les valeurs de couleur :

```css
/* Couleur principale du gradient */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Changez par vos couleurs */
background: linear-gradient(135deg, #VOTRE_COULEUR1 0%, #VOTRE_COULEUR2 100%);
```

### Modifier les textes

Les textes peuvent être modifiés directement dans le HTML ou via les paramètres du shortcode.

### Ajouter des champs personnalisés

Modifiez le fichier HTML pour ajouter de nouveaux champs, puis mettez à jour le JavaScript pour inclure les nouveaux calculs.

## 📞 Support

Pour toute question ou problème :

1. Vérifiez d'abord ce guide
2. Consultez la documentation WordPress/Elementor
3. Ouvrez une issue sur GitHub : https://github.com/bdescary/Descary/issues

## 📄 Licence

Projet open source - Libre d'utilisation

---

**Version** : 1.0.0
**Dernière mise à jour** : 2025-10-22
**Compatibilité** : WordPress 5.0+, Elementor 3.0+, Elementor Pro 3.0+
