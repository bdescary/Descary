<?php
/**
 * Plugin Name: Calculateur de Taux d'Absentéisme
 * Plugin URI: https://github.com/bdescary/Descary
 * Description: Calculateur de taux d'absentéisme pour entreprises françaises, compatible Elementor Pro
 * Version: 1.0.0
 * Author: Claude Code
 * Text Domain: calculateur-absenteisme
 */

// Empêcher l'accès direct au fichier
if (!defined('ABSPATH')) {
    exit;
}

/**
 * Enregistrement des scripts et styles
 */
function calc_absenteisme_enqueue_assets() {
    // Enregistrer le CSS
    wp_register_style(
        'calculateur-absenteisme-css',
        plugins_url('calculateur-absenteisme.css', __FILE__),
        array(),
        '1.0.0'
    );

    // Enregistrer le JavaScript
    wp_register_script(
        'calculateur-absenteisme-js',
        plugins_url('calculateur-absenteisme.js', __FILE__),
        array(),
        '1.0.0',
        true
    );
}
add_action('wp_enqueue_scripts', 'calc_absenteisme_enqueue_assets');

/**
 * Shortcode pour afficher le calculateur
 * Usage: [calculateur_absenteisme]
 */
function calculateur_absenteisme_shortcode($atts) {
    // Charger les assets
    wp_enqueue_style('calculateur-absenteisme-css');
    wp_enqueue_script('calculateur-absenteisme-js');

    // Attributs par défaut
    $atts = shortcode_atts(array(
        'titre' => 'Calculateur de Taux d\'Absentéisme',
        'sous_titre' => 'Conforme aux normes françaises du droit du travail'
    ), $atts);

    // Buffer de sortie
    ob_start();
    ?>
    <div class="calc-absenteisme-wrapper">
        <div class="calc-absenteisme-container">
            <div class="calc-absenteisme-header">
                <h1>📊 <?php echo esc_html($atts['titre']); ?></h1>
                <p class="calc-absenteisme-subtitle"><?php echo esc_html($atts['sous_titre']); ?></p>
            </div>

            <div class="calc-absenteisme-main-layout">
                <div class="calc-absenteisme-left-column">
                    <form id="calculateurAbsenteismeForm">
                        <div class="calc-absenteisme-section">
                            <div class="calc-absenteisme-section-title">1. Période d'analyse</div>
                            <div class="calc-absenteisme-grid">
                                <div class="calc-absenteisme-form-group">
                                    <label for="calcAbsPeriodType">Type de période</label>
                                    <select id="calcAbsPeriodType">
                                        <option value="mensuel">Mensuel</option>
                                        <option value="trimestriel">Trimestriel</option>
                                        <option value="annuel">Annuel</option>
                                        <option value="personnalise">Personnalisé</option>
                                    </select>
                                </div>
                                <div class="calc-absenteisme-form-group" id="calcAbsCustomPeriodGroup" style="display: none;">
                                    <label for="calcAbsCustomDays">Nombre de jours de la période</label>
                                    <input type="number" id="calcAbsCustomDays" min="1" value="30">
                                </div>
                            </div>
                        </div>

                        <div class="calc-absenteisme-section">
                            <div class="calc-absenteisme-section-title">2. Effectif et temps de travail</div>
                            <div class="calc-absenteisme-grid">
                                <div class="calc-absenteisme-form-group">
                                    <label for="calcAbsEmployees">Nombre de salariés</label>
                                    <input type="number" id="calcAbsEmployees" min="1" value="10" required>
                                    <div class="calc-absenteisme-input-hint">Effectif moyen sur la période</div>
                                </div>
                                <div class="calc-absenteisme-form-group">
                                    <label for="calcAbsWeeklyHours">Heures hebdomadaires (par salarié)</label>
                                    <input type="number" id="calcAbsWeeklyHours" min="1" max="48" value="35" step="0.5" required>
                                    <div class="calc-absenteisme-input-hint">Durée légale : 35h en France</div>
                                </div>
                            </div>
                        </div>

                        <div class="calc-absenteisme-section">
                            <div class="calc-absenteisme-section-title">3. Absences (en heures ou en jours)</div>
                            <div class="calc-absenteisme-form-group">
                                <label for="calcAbsInputMode">Mode de saisie</label>
                                <select id="calcAbsInputMode">
                                    <option value="heures">En heures</option>
                                    <option value="jours">En jours</option>
                                </select>
                            </div>

                            <div id="calcAbsHeuresMode">
                                <div class="calc-absenteisme-form-group">
                                    <label for="calcAbsAbsenceHours">Total des heures d'absence</label>
                                    <input type="number" id="calcAbsAbsenceHours" min="0" value="0" step="0.5">
                                    <div class="calc-absenteisme-input-hint">Somme de toutes les absences sur la période</div>
                                </div>
                            </div>

                            <div id="calcAbsJoursMode" class="calc-absenteisme-hidden">
                                <div class="calc-absenteisme-form-group">
                                    <label for="calcAbsAbsenceDays">Total des jours d'absence</label>
                                    <input type="number" id="calcAbsAbsenceDays" min="0" value="0" step="0.5">
                                    <div class="calc-absenteisme-input-hint">Nombre de jours ouvrés d'absence</div>
                                </div>
                            </div>

                            <div class="calc-absenteisme-absence-types">
                                <label>
                                    <input type="checkbox" id="calcAbsShowDetails">
                                    Afficher le détail par type d'absence
                                </label>

                                <div id="calcAbsDetailsSection" class="calc-absenteisme-hidden" style="margin-top: 15px;">
                                    <div class="calc-absenteisme-absence-type-row">
                                        <label>Maladie ordinaire</label>
                                        <input type="number" id="calcAbsMaladie" min="0" value="0" step="0.5">
                                    </div>
                                    <div class="calc-absenteisme-absence-type-row">
                                        <label>Accident du travail / Maladie professionnelle</label>
                                        <input type="number" id="calcAbsAccident" min="0" value="0" step="0.5">
                                    </div>
                                    <div class="calc-absenteisme-absence-type-row">
                                        <label>Congés sans solde</label>
                                        <input type="number" id="calcAbsCongesSansSolde" min="0" value="0" step="0.5">
                                    </div>
                                    <div class="calc-absenteisme-absence-type-row">
                                        <label>Absences injustifiées</label>
                                        <input type="number" id="calcAbsInjustifiees" min="0" value="0" step="0.5">
                                    </div>
                                    <div class="calc-absenteisme-absence-type-row">
                                        <label>Autres absences</label>
                                        <input type="number" id="calcAbsAutres" min="0" value="0" step="0.5">
                                    </div>
                                    <div class="calc-absenteisme-input-hint" style="margin-top: 10px;">
                                        Note: Les congés payés légaux ne sont généralement pas comptabilisés dans l'absentéisme
                                    </div>
                                </div>
                            </div>
                        </div>

                        <button type="submit" class="calc-absenteisme-btn">Calculer le taux d'absentéisme</button>
                    </form>
                </div>

                <div class="calc-absenteisme-right-column">
                    <div class="calc-absenteisme-info-box">
                        <h3>📌 Formule de calcul</h3>
                        <p>
                            <strong>Taux d'absentéisme = (Heures d'absence / Heures théoriques) × 100</strong><br>
                            Mesure l'absentéisme dans votre entreprise selon les standards français (maladie, accidents du travail, congés sans solde, etc.).
                        </p>
                    </div>

                    <div id="calcAbsResults" class="calc-absenteisme-results">
                        <div class="calc-absenteisme-main-result">
                            <div class="label">Taux d'absentéisme</div>
                            <div class="value" id="calcAbsMainRate">0%</div>
                        </div>

                        <div class="calc-absenteisme-result-item">
                            <span class="calc-absenteisme-result-label">Heures théoriques travaillées</span>
                            <span class="calc-absenteisme-result-value" id="calcAbsThericalHours">0 h</span>
                        </div>

                        <div class="calc-absenteisme-result-item">
                            <span class="calc-absenteisme-result-label">Heures d'absence totales</span>
                            <span class="calc-absenteisme-result-value" id="calcAbsTotalAbsence">0 h</span>
                        </div>

                        <div class="calc-absenteisme-result-item">
                            <span class="calc-absenteisme-result-label">Nombre de salariés</span>
                            <span class="calc-absenteisme-result-value" id="calcAbsDisplayEmployees">0</span>
                        </div>

                        <div class="calc-absenteisme-result-item">
                            <span class="calc-absenteisme-result-label">Période analysée</span>
                            <span class="calc-absenteisme-result-value" id="calcAbsDisplayPeriod">-</span>
                        </div>

                        <div id="calcAbsDetailsResults" class="calc-absenteisme-hidden" style="margin-top: 20px;">
                            <h3 style="margin-bottom: 15px; color: #333;">Détail par type d'absence</h3>
                            <div id="calcAbsDetailsContent"></div>
                        </div>

                        <div id="calcAbsInterpretation" class="calc-absenteisme-interpretation"></div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <?php
    return ob_get_clean();
}
add_shortcode('calculateur_absenteisme', 'calculateur_absenteisme_shortcode');

/**
 * Support pour Elementor
 */
function calc_absenteisme_elementor_support() {
    if (did_action('elementor/loaded')) {
        // Enregistrer le shortcode comme widget Elementor
        add_action('elementor/widgets/widgets_registered', function() {
            // Le shortcode sera automatiquement disponible dans Elementor
        });
    }
}
add_action('init', 'calc_absenteisme_elementor_support');
