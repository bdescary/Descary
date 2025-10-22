# Quiz d'Évaluation des Besoins - Medicat Partner

## 📋 Description

Quiz interactif d'évaluation de la maturité en gestion de l'absentéisme et Qualité de Vie et des Conditions de Travail (QVCT) pour les entreprises françaises.

Ce quiz permet aux prospects de Medicat Partner d'évaluer leur situation actuelle et de recevoir des recommandations personnalisées.

## 🎯 Objectifs

- **Évaluer** la situation actuelle de l'entreprise en matière de prévention de l'absentéisme
- **Mesurer** le niveau de maturité à travers 5 catégories clés
- **Fournir** des recommandations personnalisées basées sur les résultats
- **Générer** des leads qualifiés en phase de découverte

## 📊 Fonctionnalités

### 1. Collecte d'informations
- Nom de l'entreprise
- Contact (nom et email)
- Taille de l'entreprise
- Secteur d'activité

### 2. Évaluation en 5 catégories

Le quiz évalue l'entreprise sur **5 domaines clés** :

1. **Mesure de l'absentéisme** (3 questions)
   - Taux d'absentéisme actuel
   - Suivi des indicateurs
   - Analyse des causes

2. **Qualité de Vie au Travail** (3 questions)
   - Politique QVCT
   - Satisfaction des collaborateurs
   - Équilibre vie pro/perso

3. **Management & Leadership** (3 questions)
   - Formation des managers
   - Détection des signaux faibles
   - Parcours de carrière diversifiés

4. **Prévention des risques** (3 questions)
   - Document Unique d'Évaluation des Risques
   - Prévention des RPS
   - Accompagnement retour après arrêt

5. **Engagement des collaborateurs** (3 questions)
   - Niveau d'engagement
   - Taux de turnover
   - Communication et transparence

### 3. Système de scoring

- **Score global** : de 0 à 100 points
- **Score par catégorie** : visualisation en barres de progression
- **4 niveaux de maturité** :
  - 🚀 **Débutant** (0-39%) : Structuration nécessaire
  - ⚠️ **Intermédiaire** (40-59%) : Démarche entamée
  - ✅ **Avancé** (60-79%) : Bonnes pratiques en place
  - 🌟 **Expert** (80-100%) : Modèle d'excellence

### 4. Recommandations personnalisées

Le système génère automatiquement des recommandations adaptées selon :
- Le score global obtenu
- Les scores par catégorie
- Les priorités identifiées (Haute, Moyenne, Basse)

Chaque recommandation inclut :
- Un titre explicite
- Une description détaillée
- Le service Medicat Partner recommandé
- Un niveau de priorité

### 5. Call-to-Action

- Lien direct vers le formulaire de contact Medicat Partner
- Envoi automatique d'un rapport détaillé par email (à configurer)

## 🎨 Design et UX

### Interface moderne et professionnelle
- Design responsive (mobile-first)
- Animations fluides
- Barre de progression visuelle
- Palette de couleurs professionnelle
- Gradients attractifs

### Expérience utilisateur optimisée
- Navigation intuitive (Précédent/Suivant)
- Validation des formulaires
- Feedback visuel sur les sélections
- Présentation claire des résultats

## 🚀 Installation et Utilisation

### Option 1 : Fichier HTML autonome
Le quiz est entièrement contenu dans un fichier HTML unique (`quiz-evaluation-medicat.html`) avec CSS et JavaScript intégrés.

```bash
# Ouvrir directement dans un navigateur
open quiz-evaluation-medicat.html
```

### Option 2 : Intégration dans un site existant

#### Méthode A : iFrame
```html
<iframe src="quiz-evaluation-medicat.html"
        width="100%"
        height="800px"
        frameborder="0">
</iframe>
```

#### Méthode B : Intégration directe
Copier le contenu du quiz dans une page de votre site WordPress, Wix, ou autre CMS.

### Option 3 : Hébergement web
Héberger le fichier sur votre serveur web ou un service d'hébergement.

```bash
# Exemple avec un serveur Python simple
python3 -m http.server 8000
# Accéder à http://localhost:8000/quiz-evaluation-medicat.html
```

## 📈 Tracking et Analytics

### Données collectées
Le quiz collecte et affiche en console (pour test) :
- Informations entreprise (nom, contact, taille, secteur)
- Réponses aux 15 questions
- Scores par catégorie
- Score global
- Niveau de maturité

### Intégration recommandée

Pour exploiter pleinement le quiz, il est recommandé d'intégrer :

1. **Google Analytics / Tag Manager**
```javascript
// À ajouter dans la fonction submitQuiz()
gtag('event', 'quiz_completed', {
    'score': totalScore,
    'level': level,
    'company_size': userInfo.companySize
});
```

2. **CRM (HubSpot, Salesforce, etc.)**
```javascript
// Envoi des données au CRM
fetch('https://votre-api.com/leads', {
    method: 'POST',
    body: JSON.stringify({ userInfo, score, categoryScores })
});
```

3. **Email automation**
```javascript
// Envoi du rapport par email
fetch('https://votre-api.com/send-report', {
    method: 'POST',
    body: JSON.stringify({ email: userInfo.contactEmail, results })
});
```

## 🔧 Personnalisation

### Modifier les questions
Éditer l'objet `quizData` dans le JavaScript :

```javascript
const quizData = {
    categories: { ... },
    questions: [
        {
            id: 1,
            category: "absenteisme",
            text: "Votre question ici ?",
            options: [
                { text: "Réponse 1", points: 25 },
                { text: "Réponse 2", points: 15 },
                // ...
            ]
        }
    ]
};
```

### Modifier les couleurs
Éditer les variables CSS dans `:root` :

```css
:root {
    --primary-color: #0066cc;
    --secondary-color: #004999;
    --accent-color: #00a3e0;
    /* ... */
}
```

### Modifier les recommandations
Éditer la fonction `getRecommendationForCategory()` pour adapter les recommandations à vos services.

## 📱 Compatibilité

- ✅ Chrome / Edge (dernières versions)
- ✅ Firefox (dernières versions)
- ✅ Safari (dernières versions)
- ✅ Mobile (iOS / Android)
- ✅ Tablettes

## 🔐 Conformité RGPD

⚠️ **Important** : Le quiz collecte des données personnelles (nom, email, entreprise).

### À implémenter :
1. **Consentement explicite**
   - Ajouter une checkbox de consentement RGPD
   - Lien vers la politique de confidentialité

2. **Transparence**
   - Informer sur l'utilisation des données
   - Durée de conservation
   - Droits des utilisateurs (accès, rectification, suppression)

3. **Sécurité**
   - Transmission HTTPS obligatoire
   - Chiffrement des données sensibles
   - Stockage sécurisé

### Exemple d'ajout de consentement :
```html
<div class="form-group">
    <label>
        <input type="checkbox" id="rgpdConsent" required>
        J'accepte que mes données soient traitées par Medicat Partner
        conformément à la <a href="/politique-confidentialite">politique de confidentialité</a>
    </label>
</div>
```

## 📊 Métriques de succès

### KPIs à suivre :
- **Taux de complétion** : % d'utilisateurs qui finissent le quiz
- **Taux de conversion** : % qui cliquent sur "Contactez-nous"
- **Répartition des scores** : Distribution des niveaux de maturité
- **Catégories faibles** : Domaines où les prospects ont le plus besoin d'aide
- **Origine du trafic** : Sources qui génèrent le plus de complétions

## 🎯 Optimisations futures

### Phase 2 (recommandé) :
- [ ] Connexion API backend pour sauvegarder les résultats
- [ ] Envoi automatique du rapport PDF par email
- [ ] Création automatique de lead dans le CRM
- [ ] A/B testing sur les questions et recommandations
- [ ] Version multilingue (anglais)
- [ ] Comparaison avec les benchmarks sectoriels
- [ ] Partage des résultats sur les réseaux sociaux

### Phase 3 (avancé) :
- [ ] Dashboard admin pour analyser les résultats
- [ ] Scoring prédictif avec Machine Learning
- [ ] Parcours personnalisé selon les réponses initiales
- [ ] Intégration chatbot pour questions
- [ ] Module de prise de rendez-vous intégré

## 📞 Support

Pour toute question ou personnalisation :
- 🌐 Site web : https://www.medicat-partner.fr
- 📧 Email : contact@medicat-partner.fr
- 📱 Téléphone : [À compléter]

## 📄 Licence

© 2024 Medicat Partner - Tous droits réservés

---

**Créé pour Medicat Partner**
Expert en prévention de l'absentéisme depuis 36 ans
