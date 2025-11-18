/**
 * Serveur Backend pour l'Extracteur d'Avis Google Business Profile
 *
 * Ce serveur agit comme proxy pour l'API Google Places afin d'éviter
 * les problèmes CORS et de sécuriser la clé API.
 *
 * Installation :
 * npm install express cors axios dotenv
 *
 * Utilisation :
 * 1. Créez un fichier .env avec votre GOOGLE_API_KEY
 * 2. Lancez le serveur : node server.js
 * 3. Le serveur sera accessible sur http://localhost:3000
 */

const express = require('express');
const cors = require('cors');
const axios = require('axios');
require('dotenv').config();

const app = express();

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static('.')); // Servir les fichiers statiques du dossier courant

// Configuration
const GOOGLE_API_KEY = process.env.GOOGLE_API_KEY;
const PORT = process.env.PORT || 3000;

// Vérification de la clé API au démarrage
if (!GOOGLE_API_KEY) {
    console.error('❌ ERREUR : GOOGLE_API_KEY non définie dans le fichier .env');
    console.log('Créez un fichier .env avec : GOOGLE_API_KEY=votre_cle_api');
    process.exit(1);
}

/**
 * Route : Rechercher un établissement par nom et ville
 * GET /api/search?query=Restaurant+Le+Gourmet+Paris
 */
app.get('/api/search', async (req, res) => {
    try {
        const { query } = req.query;

        if (!query) {
            return res.status(400).json({ error: 'Paramètre "query" manquant' });
        }

        console.log(`🔍 Recherche : ${query}`);

        const url = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json';
        const response = await axios.get(url, {
            params: {
                input: query,
                inputtype: 'textquery',
                fields: 'place_id,name,formatted_address',
                key: GOOGLE_API_KEY
            }
        });

        if (response.data.status === 'OK' && response.data.candidates.length > 0) {
            res.json({
                success: true,
                results: response.data.candidates
            });
        } else {
            res.json({
                success: false,
                message: 'Aucun établissement trouvé',
                status: response.data.status
            });
        }

    } catch (error) {
        console.error('❌ Erreur recherche:', error.message);
        res.status(500).json({
            error: 'Erreur lors de la recherche',
            details: error.message
        });
    }
});

/**
 * Route : Récupérer les détails et avis d'un établissement
 * GET /api/reviews/:placeId
 */
app.get('/api/reviews/:placeId', async (req, res) => {
    try {
        const { placeId } = req.params;

        if (!placeId) {
            return res.status(400).json({ error: 'Place ID manquant' });
        }

        console.log(`📊 Récupération des avis pour Place ID : ${placeId}`);

        const url = 'https://maps.googleapis.com/maps/api/place/details/json';
        const response = await axios.get(url, {
            params: {
                place_id: placeId,
                fields: 'name,rating,user_ratings_total,reviews,formatted_address,formatted_phone_number,website',
                key: GOOGLE_API_KEY,
                language: 'fr'
            }
        });

        if (response.data.status === 'OK') {
            const result = response.data.result;

            // Formater les avis pour l'application
            const reviews = (result.reviews || []).map(review => ({
                author: review.author_name,
                rating: review.rating,
                text: review.text,
                date: new Date(review.time * 1000).toISOString().split('T')[0],
                relative_time: review.relative_time_description,
                profile_photo: review.profile_photo_url
            }));

            res.json({
                success: true,
                business: {
                    name: result.name,
                    address: result.formatted_address,
                    phone: result.formatted_phone_number,
                    website: result.website,
                    rating: result.rating,
                    total_ratings: result.user_ratings_total
                },
                reviews: reviews,
                total_reviews: reviews.length
            });

            console.log(`✅ ${reviews.length} avis récupérés pour ${result.name}`);

        } else {
            res.status(404).json({
                success: false,
                message: 'Établissement non trouvé',
                status: response.data.status
            });
        }

    } catch (error) {
        console.error('❌ Erreur récupération avis:', error.message);
        res.status(500).json({
            error: 'Erreur lors de la récupération des avis',
            details: error.message
        });
    }
});

/**
 * Route : Page d'accueil
 */
app.get('/', (req, res) => {
    res.send(`
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>API Google Reviews - Serveur Backend</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    max-width: 800px;
                    margin: 50px auto;
                    padding: 20px;
                    background: #f5f5f5;
                }
                .container {
                    background: white;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }
                h1 { color: #667eea; }
                .endpoint {
                    background: #f8f9fa;
                    padding: 15px;
                    margin: 10px 0;
                    border-radius: 5px;
                    border-left: 4px solid #667eea;
                }
                code {
                    background: #e9ecef;
                    padding: 2px 6px;
                    border-radius: 3px;
                    font-family: 'Courier New', monospace;
                }
                .status {
                    display: inline-block;
                    padding: 5px 15px;
                    background: #28a745;
                    color: white;
                    border-radius: 20px;
                    font-weight: bold;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🚀 Serveur API Google Reviews</h1>
                <p><span class="status">✓ En ligne</span></p>

                <h2>📍 Endpoints disponibles :</h2>

                <div class="endpoint">
                    <strong>GET /api/search</strong>
                    <p>Rechercher un établissement par nom</p>
                    <p>Paramètres : <code>query</code> (nom de l'établissement)</p>
                    <p>Exemple : <code>/api/search?query=Restaurant+Paris</code></p>
                </div>

                <div class="endpoint">
                    <strong>GET /api/reviews/:placeId</strong>
                    <p>Récupérer les avis d'un établissement</p>
                    <p>Paramètres : <code>placeId</code> (ID Google Places)</p>
                    <p>Exemple : <code>/api/reviews/ChIJN1t_tDeuEmsRUsoyG83frY4</code></p>
                </div>

                <h2>📝 Utilisation :</h2>
                <ol>
                    <li>Ouvrez <a href="/google-reviews-scraper.html">google-reviews-scraper.html</a></li>
                    <li>Entrez votre clé API et Place ID</li>
                    <li>Cliquez sur "Récupérer les avis"</li>
                </ol>

                <h2>⚙️ Configuration :</h2>
                <p>Clé API configurée : <strong>${GOOGLE_API_KEY ? '✓ Oui' : '✗ Non'}</strong></p>
                <p>Port : <strong>${PORT}</strong></p>
            </div>
        </body>
        </html>
    `);
});

/**
 * Route : Status de santé du serveur
 */
app.get('/health', (req, res) => {
    res.json({
        status: 'OK',
        timestamp: new Date().toISOString(),
        api_configured: !!GOOGLE_API_KEY
    });
});

// Gestion des erreurs 404
app.use((req, res) => {
    res.status(404).json({
        error: 'Route non trouvée',
        available_routes: [
            'GET /api/search?query=...',
            'GET /api/reviews/:placeId',
            'GET /health'
        ]
    });
});

// Démarrage du serveur
app.listen(PORT, () => {
    console.log('\n========================================');
    console.log('🚀 Serveur démarré avec succès !');
    console.log('========================================');
    console.log(`📍 URL : http://localhost:${PORT}`);
    console.log(`🔑 API Google Places : ${GOOGLE_API_KEY ? '✓ Configurée' : '✗ Non configurée'}`);
    console.log('========================================\n');
    console.log('📚 Endpoints disponibles :');
    console.log(`   - GET  /`);
    console.log(`   - GET  /api/search?query=...`);
    console.log(`   - GET  /api/reviews/:placeId`);
    console.log(`   - GET  /health`);
    console.log('\n💡 Appuyez sur Ctrl+C pour arrêter le serveur\n');
});

// Gestion de l'arrêt gracieux
process.on('SIGINT', () => {
    console.log('\n👋 Arrêt du serveur...');
    process.exit(0);
});

module.exports = app;
