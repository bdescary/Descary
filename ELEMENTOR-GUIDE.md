# 🎨 Guide d'Intégration WordPress Elementor

## ✅ Quiz Optimisé pour Elementor

Le fichier **quiz-elementor-version.html** a été spécialement optimisé pour fonctionner dans WordPress avec Elementor.

### Différences avec la version standard :

✅ **Styles CSS encapsulés** - Préfixés avec `.mq-` pour éviter les conflits
✅ **JavaScript dans un namespace** - `MedicatQuiz` pour éviter les conflits globaux
✅ **IDs uniques** - Préfixés avec `mq` (ex: `mqWelcome`, `mqQuizSection`)
✅ **Compatibilité thèmes WordPress** - Styles isolés du thème
✅ **Responsive** - Fonctionne parfaitement sur mobile/tablette

---

## 📝 Méthode 1 : Widget HTML Elementor (Recommandé)

### Étape 1 : Créer une page dans WordPress

1. Dans WordPress, allez dans **Pages → Ajouter**
2. Nommez votre page (ex: "Quiz d'Évaluation")
3. Cliquez sur **Modifier avec Elementor**

### Étape 2 : Ajouter le widget HTML

1. Dans Elementor, cherchez le widget **HTML** dans le panneau de gauche
2. Glissez-déposez le widget **HTML** sur votre page
3. Ouvrez le fichier `quiz-elementor-version.html`
4. Copiez **TOUT le contenu** du fichier (Ctrl+A, Ctrl+C)
5. Collez-le dans le widget HTML d'Elementor
6. Cliquez sur **Mettre à jour**

### Étape 3 : Publier

1. Cliquez sur **Publier** en bas à gauche
2. Testez votre page !

---

## 🎯 Méthode 2 : Shortcode WordPress (Pour utilisateurs avancés)

Cette méthode permet de réutiliser le quiz sur plusieurs pages avec un simple shortcode `[medicat_quiz]`.

### Étape 1 : Ajouter le code dans functions.php

Allez dans **Apparence → Éditeur de thème → functions.php** (ou utilisez un plugin comme "Code Snippets")

```php
<?php
// Shortcode Quiz Medicat Partner
function medicat_quiz_shortcode() {
    ob_start();
    include(get_stylesheet_directory() . '/quiz-medicat.php');
    return ob_get_clean();
}
add_shortcode('medicat_quiz', 'medicat_quiz_shortcode');
?>
```

### Étape 2 : Créer le fichier quiz-medicat.php

Dans votre thème enfant, créez un fichier `quiz-medicat.php` et collez-y le contenu de `quiz-elementor-version.html`.

### Étape 3 : Utiliser le shortcode

Dans n'importe quelle page Elementor :
1. Ajoutez un widget **Shortcode**
2. Entrez : `[medicat_quiz]`
3. Publiez !

---

## 🔧 Méthode 3 : Plugin Custom (Pour développeurs)

Créez un plugin WordPress personnalisé pour une meilleure gestion.

### Étape 1 : Créer le plugin

Créez un dossier `/wp-content/plugins/medicat-quiz/` avec ces fichiers :

**medicat-quiz.php** (fichier principal)
```php
<?php
/**
 * Plugin Name: Medicat Partner - Quiz d'Évaluation
 * Description: Quiz interactif d'évaluation de la maturité en gestion de l'absentéisme
 * Version: 1.0
 * Author: Medicat Partner
 */

// Enregistrer le shortcode
function medicat_quiz_shortcode() {
    ob_start();
    include(plugin_dir_path(__FILE__) . 'templates/quiz.php');
    return ob_get_clean();
}
add_shortcode('medicat_quiz', 'medicat_quiz_shortcode');

// Enregistrer un widget Elementor personnalisé (optionnel)
function register_medicat_quiz_widget($widgets_manager) {
    require_once(plugin_dir_path(__FILE__) . 'widgets/quiz-widget.php');
    $widgets_manager->register(new \Medicat_Quiz_Widget());
}
add_action('elementor/widgets/register', 'register_medicat_quiz_widget');
?>
```

**templates/quiz.php**
```php
<?php
// Copier le contenu de quiz-elementor-version.html ici
?>
```

### Étape 2 : Activer le plugin

1. Allez dans **Extensions → Extensions installées**
2. Activez **Medicat Partner - Quiz d'Évaluation**
3. Utilisez le shortcode `[medicat_quiz]` partout !

---

## 🎨 Personnalisation dans Elementor

### Changer les couleurs

Dans le code HTML du widget, trouvez cette section (lignes 20-27) :

```css
.medicat-quiz-wrapper {
    --mq-primary: #0066cc;      /* Couleur principale - CHANGEZ ICI */
    --mq-secondary: #004999;    /* Couleur secondaire */
    --mq-accent: #00a3e0;       /* Couleur accent */
    /* ... */
}
```

**Astuce** : Utilisez les couleurs de votre thème WordPress pour une cohérence visuelle.

### Ajuster la largeur

Trouvez cette ligne (ligne 5) :

```css
#medicat-quiz-container {
    max-width: 900px;  /* CHANGEZ ICI pour ajuster la largeur */
    margin: 40px auto;
}
```

### Modifier les marges

```css
#medicat-quiz-container {
    margin: 40px auto;  /* CHANGEZ ICI : 40px en haut/bas, auto à gauche/droite */
}
```

---

## 🔌 Intégrations WordPress

### 1. Formulaire de contact (Contact Form 7)

Remplacez le CTA final par un formulaire Contact Form 7 :

```html
<!-- Remplacer la section .mq-cta par : -->
<div class="mq-cta">
    <h3>Prêt à transformer votre entreprise ?</h3>
    <?php echo do_shortcode('[contact-form-7 id="123" title="Contact Quiz"]'); ?>
</div>
```

### 2. WPForms / Gravity Forms

```html
<?php echo do_shortcode('[wpforms id="123"]'); ?>
<!-- ou -->
<?php echo do_shortcode('[gravityform id="1" title="false"]'); ?>
```

### 3. Google Analytics (MonsterInsights ou autre)

Le code JavaScript actuel utilise `console.log()`. Modifiez la fonction `displayResults()` :

```javascript
// Trouvez cette ligne à la fin de displayResults() :
console.log('Résultats:', { userInfo, score, categoryScores, level });

// Remplacez par :
// Pour MonsterInsights
if (typeof gtag !== 'undefined') {
    gtag('event', 'quiz_completed', {
        'event_category': 'Quiz Medicat',
        'event_label': level,
        'value': score
    });
}

// Pour Google Analytics classique
if (typeof ga !== 'undefined') {
    ga('send', 'event', 'Quiz Medicat', 'completed', level, score);
}
```

### 4. Envoi des données vers WordPress

Créez un endpoint AJAX WordPress pour sauvegarder les résultats :

**Dans functions.php :**

```php
// Endpoint AJAX pour sauvegarder les résultats du quiz
function save_medicat_quiz_results() {
    global $wpdb;

    $data = json_decode(file_get_contents('php://input'), true);

    $table_name = $wpdb->prefix . 'medicat_quiz_results';

    $wpdb->insert(
        $table_name,
        array(
            'company_name' => sanitize_text_field($data['userInfo']['companyName']),
            'contact_name' => sanitize_text_field($data['userInfo']['contactName']),
            'contact_email' => sanitize_email($data['userInfo']['contactEmail']),
            'company_size' => sanitize_text_field($data['userInfo']['companySize']),
            'sector' => sanitize_text_field($data['userInfo']['sector']),
            'score' => intval($data['score']),
            'level' => sanitize_text_field($data['level']),
            'category_scores' => json_encode($data['categoryScores']),
            'created_at' => current_time('mysql')
        )
    );

    // Envoyer un email à l'équipe commerciale
    $to = 'commercial@medicat-partner.fr';
    $subject = 'Nouveau lead - Quiz d\'évaluation';
    $message = sprintf(
        "Nouveau prospect qualifié :\n\nEntreprise : %s\nContact : %s\nEmail : %s\nScore : %d/100\nNiveau : %s",
        $data['userInfo']['companyName'],
        $data['userInfo']['contactName'],
        $data['userInfo']['contactEmail'],
        $data['score'],
        $data['level']
    );
    wp_mail($to, $subject, $message);

    wp_send_json_success(array('message' => 'Résultats enregistrés'));
}
add_action('wp_ajax_save_quiz_results', 'save_medicat_quiz_results');
add_action('wp_ajax_nopriv_save_quiz_results', 'save_medicat_quiz_results');

// Créer la table à l'activation
function create_medicat_quiz_table() {
    global $wpdb;
    $table_name = $wpdb->prefix . 'medicat_quiz_results';
    $charset_collate = $wpdb->get_charset_collate();

    $sql = "CREATE TABLE IF NOT EXISTS $table_name (
        id mediumint(9) NOT NULL AUTO_INCREMENT,
        company_name varchar(255) NOT NULL,
        contact_name varchar(255) NOT NULL,
        contact_email varchar(255) NOT NULL,
        company_size varchar(50) NOT NULL,
        sector varchar(255) NOT NULL,
        score int(3) NOT NULL,
        level varchar(50) NOT NULL,
        category_scores text NOT NULL,
        created_at datetime DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY  (id)
    ) $charset_collate;";

    require_once(ABSPATH . 'wp-admin/includes/upgrade.php');
    dbDelta($sql);
}
register_activation_hook(__FILE__, 'create_medicat_quiz_table');
```

**Dans le JavaScript du quiz :**

```javascript
// Trouvez la fonction displayResults() et ajoutez à la fin :

// Envoyer les données à WordPress
fetch('/wp-admin/admin-ajax.php?action=save_quiz_results', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        userInfo: userInfo,
        score: score,
        level: level,
        categoryScores: categoryScores
    })
})
.then(response => response.json())
.then(data => console.log('Résultats sauvegardés:', data))
.catch(error => console.error('Erreur:', error));
```

---

## 🎯 Dashboard Admin WordPress (Bonus)

Ajoutez une page d'administration pour voir les résultats :

```php
// Ajouter un menu dans l'admin WordPress
function medicat_quiz_admin_menu() {
    add_menu_page(
        'Résultats Quiz Medicat',
        'Quiz Medicat',
        'manage_options',
        'medicat-quiz-results',
        'medicat_quiz_results_page',
        'dashicons-clipboard',
        30
    );
}
add_action('admin_menu', 'medicat_quiz_admin_menu');

// Page d'affichage des résultats
function medicat_quiz_results_page() {
    global $wpdb;
    $table_name = $wpdb->prefix . 'medicat_quiz_results';
    $results = $wpdb->get_results("SELECT * FROM $table_name ORDER BY created_at DESC LIMIT 100");

    echo '<div class="wrap">';
    echo '<h1>Résultats des Quiz - Medicat Partner</h1>';
    echo '<table class="wp-list-table widefat fixed striped">';
    echo '<thead><tr>';
    echo '<th>Date</th><th>Entreprise</th><th>Contact</th><th>Email</th><th>Taille</th><th>Score</th><th>Niveau</th>';
    echo '</tr></thead><tbody>';

    foreach ($results as $result) {
        echo '<tr>';
        echo '<td>' . date('d/m/Y H:i', strtotime($result->created_at)) . '</td>';
        echo '<td>' . esc_html($result->company_name) . '</td>';
        echo '<td>' . esc_html($result->contact_name) . '</td>';
        echo '<td><a href="mailto:' . esc_attr($result->contact_email) . '">' . esc_html($result->contact_email) . '</a></td>';
        echo '<td>' . esc_html($result->company_size) . '</td>';
        echo '<td><strong>' . $result->score . '/100</strong></td>';
        echo '<td>' . esc_html($result->level) . '</td>';
        echo '</tr>';
    }

    echo '</tbody></table>';
    echo '</div>';
}
```

---

## 🐛 Résolution de Problèmes

### Le quiz ne s'affiche pas

**Solution 1** : Vérifiez que vous avez copié **TOUT** le code depuis `<div id="medicat-quiz-container">` jusqu'à `</div>` final.

**Solution 2** : Désactivez temporairement les autres plugins pour identifier les conflits.

**Solution 3** : Utilisez le widget HTML en mode "Full Width" dans Elementor.

### Les styles ne s'appliquent pas correctement

**Cause** : Conflit avec le thème WordPress.

**Solution** : Augmentez la spécificité CSS en ajoutant `!important` :

```css
#medicat-quiz-container {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
    max-width: 900px !important;
}
```

### Le JavaScript ne fonctionne pas

**Cause** : jQuery de WordPress interfère.

**Solution** : Le code utilise du JavaScript vanilla (pas de jQuery), il devrait fonctionner. Vérifiez la console navigateur (F12) pour les erreurs.

### Le quiz dépasse de la colonne Elementor

**Solution** : Ajustez `max-width` dans le CSS :

```css
#medicat-quiz-container {
    max-width: 100% !important;  /* Au lieu de 900px */
    margin: 20px auto;
}
```

---

## ✅ Checklist de Mise en Production

- [ ] Quiz intégré dans une page WordPress
- [ ] Test sur desktop, tablette, mobile
- [ ] Test sur Chrome, Firefox, Safari
- [ ] Couleurs adaptées au thème WordPress
- [ ] Lien "Contactez-nous" configuré
- [ ] Google Analytics configuré (optionnel)
- [ ] Envoi des données vers CRM/Email configuré
- [ ] Consentement RGPD ajouté si nécessaire
- [ ] Test complet du parcours utilisateur
- [ ] Page publiée et accessible

---

## 📊 Optimisations WordPress Spécifiques

### Cache WordPress

Si vous utilisez un plugin de cache (WP Rocket, W3 Total Cache, etc.), excluez la page du quiz du cache pour garantir le bon fonctionnement du JavaScript.

### Lazy Loading

Désactivez le lazy loading sur la page du quiz pour éviter les problèmes d'affichage.

### Minification

Le code JavaScript est déjà optimisé. Si votre plugin de cache minifie le JS, testez bien le quiz après activation.

---

## 📞 Support

Pour toute question sur l'intégration WordPress/Elementor :
- 📧 support-technique@medicat-partner.fr
- 📚 Documentation complète : README-QUIZ.md
- 🔧 Guide technique : INTEGRATION-GUIDE.md

---

**Version Elementor créée avec succès !** ✅

Vous pouvez maintenant intégrer le quiz facilement dans WordPress avec Elementor en suivant la **Méthode 1** ci-dessus.
