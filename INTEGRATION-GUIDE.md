# Guide d'Intégration Technique - Quiz Medicat Partner

## 🔌 Options d'Intégration

### 1. Intégration CRM (Recommandé)

#### HubSpot
```javascript
// Ajouter après la fonction calculateResults()
function sendToHubSpot(userData, results) {
    const formData = {
        fields: [
            { name: 'firstname', value: userData.contactName.split(' ')[0] },
            { name: 'lastname', value: userData.contactName.split(' ')[1] || '' },
            { name: 'email', value: userData.contactEmail },
            { name: 'company', value: userData.companyName },
            { name: 'company_size', value: userData.companySize },
            { name: 'industry', value: userData.sector },
            { name: 'quiz_score', value: results.score },
            { name: 'maturity_level', value: results.level }
        ]
    };

    fetch(`https://api.hsforms.com/submissions/v3/integration/submit/{PORTAL_ID}/{FORM_GUID}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => console.log('Lead envoyé à HubSpot:', data))
    .catch(error => console.error('Erreur HubSpot:', error));
}

// Appeler dans submitQuiz()
sendToHubSpot(userInfo, { score: scorePercentage, level: level });
```

#### Salesforce
```javascript
function sendToSalesforce(userData, results) {
    const leadData = {
        FirstName: userData.contactName.split(' ')[0],
        LastName: userData.contactName.split(' ')[1] || '',
        Email: userData.contactEmail,
        Company: userData.companyName,
        NumberOfEmployees: userData.companySize,
        Industry: userData.sector,
        Quiz_Score__c: results.score,
        Maturity_Level__c: results.level,
        LeadSource: 'Quiz Evaluation'
    };

    // Utiliser votre API Salesforce
    fetch('https://your-salesforce-api.com/lead', {
        method: 'POST',
        headers: {
            'Authorization': 'Bearer YOUR_TOKEN',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(leadData)
    })
    .then(response => response.json())
    .then(data => console.log('Lead créé dans Salesforce:', data))
    .catch(error => console.error('Erreur Salesforce:', error));
}
```

### 2. Envoi d'Email Automatique

#### Avec EmailJS (Simple)
```html
<!-- Ajouter dans le <head> -->
<script src="https://cdn.emailjs.com/dist/email.min.js"></script>
<script>
    emailjs.init("YOUR_PUBLIC_KEY");
</script>
```

```javascript
function sendEmailReport(userData, results, recommendations) {
    const templateParams = {
        to_email: userData.contactEmail,
        to_name: userData.contactName,
        company_name: userData.companyName,
        score: results.score,
        level: results.level,
        recommendations: recommendations.map(r => r.title).join('\n- ')
    };

    emailjs.send('YOUR_SERVICE_ID', 'YOUR_TEMPLATE_ID', templateParams)
        .then(response => {
            console.log('Email envoyé !', response);
        })
        .catch(error => {
            console.error('Erreur email:', error);
        });
}
```

#### Avec API backend
```javascript
function sendEmailReport(userData, results) {
    fetch('https://votre-domaine.com/api/send-quiz-report', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-API-Key': 'YOUR_API_KEY'
        },
        body: JSON.stringify({
            recipient: userData.contactEmail,
            data: {
                userInfo: userData,
                score: results.score,
                level: results.level,
                categoryScores: results.categoryScores,
                recommendations: results.recommendations
            }
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Rapport envoyé:', data);
        alert('📧 Un rapport détaillé vous a été envoyé par email !');
    })
    .catch(error => console.error('Erreur:', error));
}
```

### 3. Google Analytics / Tag Manager

#### Google Analytics 4
```html
<!-- Ajouter dans le <head> -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-XXXXXXXXXX');
</script>
```

```javascript
// Tracking des événements
function trackQuizEvents(eventName, params) {
    if (typeof gtag !== 'undefined') {
        gtag('event', eventName, params);
    }
}

// Dans startQuiz()
trackQuizEvents('quiz_started', {
    company_size: userInfo.companySize,
    sector: userInfo.sector
});

// Pour chaque question
trackQuizEvents('question_answered', {
    question_id: currentQuestion + 1,
    category: question.category,
    answer_value: question.options[answers[currentQuestion]].points
});

// Dans submitQuiz()
trackQuizEvents('quiz_completed', {
    score: scorePercentage,
    maturity_level: level,
    company_size: userInfo.companySize,
    sector: userInfo.sector
});

// Quand l'utilisateur clique sur le CTA
trackQuizEvents('contact_cta_clicked', {
    score: scorePercentage,
    level: level
});
```

#### Google Tag Manager
```javascript
// Push vers le dataLayer
function pushToDataLayer(event, data) {
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push({
        'event': event,
        ...data
    });
}

// Exemples d'utilisation
pushToDataLayer('quizStarted', { companySize: userInfo.companySize });
pushToDataLayer('quizCompleted', { score: scorePercentage, level: level });
```

### 4. Webhook générique

```javascript
function sendWebhook(userData, results) {
    const webhookData = {
        event: 'quiz_completed',
        timestamp: new Date().toISOString(),
        user: {
            company: userData.companyName,
            contact: userData.contactName,
            email: userData.contactEmail,
            size: userData.companySize,
            sector: userData.sector
        },
        results: {
            score: results.score,
            level: results.level,
            categoryScores: results.categoryScores,
            recommendations: results.recommendations
        }
    };

    fetch('https://votre-webhook-url.com/quiz', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-Webhook-Secret': 'YOUR_SECRET_KEY'
        },
        body: JSON.stringify(webhookData)
    })
    .then(response => response.json())
    .then(data => console.log('Webhook envoyé:', data))
    .catch(error => console.error('Erreur webhook:', error));
}
```

### 5. Stockage local (Développement/Test)

```javascript
function saveResultsLocally(userData, results) {
    const resultsData = {
        timestamp: new Date().toISOString(),
        userInfo: userData,
        results: results
    };

    // LocalStorage
    localStorage.setItem(`quiz_${Date.now()}`, JSON.stringify(resultsData));

    // Télécharger en JSON
    const dataStr = JSON.stringify(resultsData, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `quiz-results-${userData.companyName}-${Date.now()}.json`;
    link.click();
}
```

## 🔒 Sécurité et RGPD

### Ajout du consentement RGPD

```javascript
// Modifier startQuiz() pour inclure la validation du consentement
function startQuiz() {
    // ... validations existantes ...

    // Nouvelle validation RGPD
    const rgpdConsent = document.getElementById('rgpdConsent');
    if (!rgpdConsent || !rgpdConsent.checked) {
        alert('Veuillez accepter la politique de confidentialité pour continuer');
        return;
    }

    userInfo.consentDate = new Date().toISOString();
    userInfo.consentGiven = true;

    // ... reste du code ...
}
```

```html
<!-- Ajouter dans le formulaire info-form -->
<div class="form-group" style="margin-top: 25px;">
    <label style="display: flex; align-items: start; cursor: pointer;">
        <input type="checkbox" id="rgpdConsent" required
               style="margin-right: 10px; margin-top: 5px; width: auto;">
        <span style="font-size: 0.95em; line-height: 1.5;">
            J'accepte que mes données personnelles soient utilisées par Medicat Partner
            pour me contacter au sujet de cette évaluation.
            <a href="https://www.medicat-partner.fr/politique-confidentialite"
               target="_blank" style="color: var(--primary-color);">
                Voir la politique de confidentialité
            </a>
        </span>
    </label>
</div>
```

### Protection contre le spam

```javascript
// Honeypot (champ caché)
// Ajouter dans le formulaire
<input type="text" name="website" id="website" style="display: none;" tabindex="-1" autocomplete="off">

// Vérification
function startQuiz() {
    // Anti-spam check
    if (document.getElementById('website').value !== '') {
        console.log('Spam détecté');
        return;
    }
    // ... reste du code ...
}

// Rate limiting simple (côté client)
function checkRateLimit() {
    const lastSubmission = localStorage.getItem('lastQuizSubmission');
    if (lastSubmission) {
        const timeDiff = Date.now() - parseInt(lastSubmission);
        if (timeDiff < 300000) { // 5 minutes
            alert('Veuillez attendre quelques minutes avant de soumettre un nouveau quiz');
            return false;
        }
    }
    return true;
}

function submitQuiz() {
    if (!checkRateLimit()) return;

    // ... code existant ...

    localStorage.setItem('lastQuizSubmission', Date.now().toString());
}
```

## 📊 Backend API Exemple (Node.js/Express)

```javascript
// server.js
const express = require('express');
const cors = require('cors');
const nodemailer = require('nodemailer');
const app = express();

app.use(cors());
app.use(express.json());

// Configuration email
const transporter = nodemailer.createTransport({
    host: 'smtp.example.com',
    port: 587,
    secure: false,
    auth: {
        user: process.env.SMTP_USER,
        pass: process.env.SMTP_PASS
    }
});

// Endpoint pour recevoir les résultats du quiz
app.post('/api/quiz-results', async (req, res) => {
    try {
        const { userInfo, score, level, categoryScores, recommendations } = req.body;

        // 1. Sauvegarder en base de données
        // await saveToDatabase(req.body);

        // 2. Envoyer l'email au prospect
        await sendEmailToProspect(userInfo, score, level, recommendations);

        // 3. Notifier l'équipe commerciale
        await notifySalesTeam(userInfo, score, level);

        // 4. Créer le lead dans le CRM
        // await createCRMLead(userInfo, score, level);

        res.json({ success: true, message: 'Résultats enregistrés avec succès' });
    } catch (error) {
        console.error('Erreur:', error);
        res.status(500).json({ success: false, message: 'Erreur serveur' });
    }
});

async function sendEmailToProspect(userInfo, score, level, recommendations) {
    const html = `
        <h1>Résultats de votre évaluation</h1>
        <p>Bonjour ${userInfo.contactName},</p>
        <p>Merci d'avoir complété notre quiz d'évaluation.</p>
        <h2>Vos résultats :</h2>
        <ul>
            <li><strong>Score global :</strong> ${score}/100</li>
            <li><strong>Niveau de maturité :</strong> ${level}</li>
        </ul>
        <h3>Nos recommandations :</h3>
        <ul>
            ${recommendations.map(r => `<li><strong>${r.title}</strong>: ${r.description}</li>`).join('')}
        </ul>
        <p>Un expert Medicat Partner vous contactera sous 48h.</p>
    `;

    await transporter.sendMail({
        from: '"Medicat Partner" <contact@medicat-partner.fr>',
        to: userInfo.contactEmail,
        subject: 'Vos résultats - Quiz d\'évaluation Medicat Partner',
        html: html
    });
}

async function notifySalesTeam(userInfo, score, level) {
    const priority = score < 50 ? 'HAUTE' : score < 70 ? 'MOYENNE' : 'NORMALE';

    await transporter.sendMail({
        from: '"Quiz Medicat" <noreply@medicat-partner.fr>',
        to: 'commercial@medicat-partner.fr',
        subject: `🎯 Nouveau lead quiz - ${userInfo.companyName} (Priorité: ${priority})`,
        html: `
            <h2>Nouveau prospect qualifié</h2>
            <ul>
                <li><strong>Entreprise :</strong> ${userInfo.companyName}</li>
                <li><strong>Contact :</strong> ${userInfo.contactName}</li>
                <li><strong>Email :</strong> ${userInfo.contactEmail}</li>
                <li><strong>Taille :</strong> ${userInfo.companySize}</li>
                <li><strong>Secteur :</strong> ${userInfo.sector}</li>
                <li><strong>Score :</strong> ${score}/100</li>
                <li><strong>Niveau :</strong> ${level}</li>
                <li><strong>Priorité :</strong> ${priority}</li>
            </ul>
        `
    });
}

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
```

## 🎨 Personnalisation CSS

### Modifier le thème de couleurs

```javascript
// Ajouter au début du <script>
function applyCustomTheme() {
    const root = document.documentElement;
    root.style.setProperty('--primary-color', '#0066cc');
    root.style.setProperty('--secondary-color', '#004999');
    root.style.setProperty('--accent-color', '#00a3e0');
}

// Appeler au chargement
window.addEventListener('DOMContentLoaded', applyCustomTheme);
```

### Mode sombre (optionnel)

```css
@media (prefers-color-scheme: dark) {
    :root {
        --white: #1a1a1a;
        --light-bg: #2a2a2a;
        --text-dark: #ffffff;
        --text-light: #cccccc;
        --border-color: #444444;
    }

    body {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    }
}
```

## 🧪 Tests

### Test de validation des données
```javascript
// Tests unitaires (avec Jest)
describe('Quiz Validation', () => {
    test('Email validation', () => {
        const validEmails = ['test@example.com', 'user.name@domain.co.uk'];
        const invalidEmails = ['test@', '@example.com', 'test'];

        validEmails.forEach(email => {
            expect(validateEmail(email)).toBe(true);
        });

        invalidEmails.forEach(email => {
            expect(validateEmail(email)).toBe(false);
        });
    });

    test('Score calculation', () => {
        const answers = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
        const score = calculateScore(answers);
        expect(score).toBeGreaterThanOrEqual(0);
        expect(score).toBeLessThanOrEqual(100);
    });
});
```

### Test manuel
1. Remplir le formulaire avec des données valides
2. Répondre à toutes les questions
3. Vérifier que le score s'affiche correctement
4. Vérifier que les recommandations sont pertinentes
5. Tester sur mobile et desktop
6. Vérifier la conformité RGPD

## 📦 Déploiement

### Sur serveur web classique
```bash
# Upload via FTP/SFTP
scp quiz-evaluation-medicat.html user@server:/var/www/html/quiz/
```

### Sur Netlify (gratuit)
```bash
# Via Netlify CLI
netlify deploy --prod --dir=.
```

### Sur Vercel (gratuit)
```bash
# Via Vercel CLI
vercel --prod
```

## 🆘 Troubleshooting

### Le quiz ne s'affiche pas
- Vérifier la console JavaScript (F12) pour les erreurs
- Vérifier que le fichier est bien encodé en UTF-8
- Vérifier les permissions de fichiers sur le serveur

### Les emails ne sont pas envoyés
- Vérifier la configuration SMTP
- Vérifier les logs côté serveur
- Tester avec un service de test d'email (MailHog, Mailtrap)

### Problèmes de responsive
- Tester avec les DevTools du navigateur (F12 > mode responsive)
- Vérifier la balise viewport dans le <head>
- Tester sur plusieurs devices réels

## 📞 Support Technique

Pour toute question technique sur l'intégration :
- Documentation complète : README-QUIZ.md
- Issues GitHub : [lien à définir]
- Email technique : dev@medicat-partner.fr

---

**Version 1.0** - Créé pour Medicat Partner
