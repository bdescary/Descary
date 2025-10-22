/**
 * Calculateur de Taux d'Absentéisme - JavaScript pour WordPress/Elementor
 * Version: 1.0
 */

(function() {
    'use strict';

    // Attendre que le DOM soit chargé
    document.addEventListener('DOMContentLoaded', function() {
        initCalculateurAbsenteisme();
    });

    function initCalculateurAbsenteisme() {
        // Vérifier que le formulaire existe
        const form = document.getElementById('calculateurAbsenteismeForm');
        if (!form) return;

        // Gestion de l'affichage des modes
        const periodType = document.getElementById('calcAbsPeriodType');
        if (periodType) {
            periodType.addEventListener('change', function() {
                const customGroup = document.getElementById('calcAbsCustomPeriodGroup');
                if (customGroup) {
                    customGroup.style.display = this.value === 'personnalise' ? 'block' : 'none';
                }
            });
        }

        const inputMode = document.getElementById('calcAbsInputMode');
        if (inputMode) {
            inputMode.addEventListener('change', function() {
                const heuresMode = document.getElementById('calcAbsHeuresMode');
                const joursMode = document.getElementById('calcAbsJoursMode');

                if (this.value === 'heures') {
                    heuresMode.classList.remove('calc-absenteisme-hidden');
                    joursMode.classList.add('calc-absenteisme-hidden');
                } else {
                    heuresMode.classList.add('calc-absenteisme-hidden');
                    joursMode.classList.remove('calc-absenteisme-hidden');
                }
            });
        }

        const showDetails = document.getElementById('calcAbsShowDetails');
        if (showDetails) {
            showDetails.addEventListener('change', function() {
                const detailsSection = document.getElementById('calcAbsDetailsSection');
                if (detailsSection) {
                    detailsSection.classList.toggle('calc-absenteisme-hidden', !this.checked);
                }
            });
        }

        // Fonction de calcul
        form.addEventListener('submit', function(e) {
            e.preventDefault();

            // Récupération des valeurs
            const periodTypeVal = document.getElementById('calcAbsPeriodType').value;
            const employees = parseFloat(document.getElementById('calcAbsEmployees').value);
            const weeklyHours = parseFloat(document.getElementById('calcAbsWeeklyHours').value);
            const inputModeVal = document.getElementById('calcAbsInputMode').value;
            const showDetailsVal = document.getElementById('calcAbsShowDetails').checked;

            // Calcul du nombre de semaines
            let weeks;
            switch(periodTypeVal) {
                case 'mensuel':
                    weeks = 4.33;
                    break;
                case 'trimestriel':
                    weeks = 13;
                    break;
                case 'annuel':
                    weeks = 52;
                    break;
                case 'personnalise':
                    weeks = parseFloat(document.getElementById('calcAbsCustomDays').value) / 7;
                    break;
            }

            // Heures théoriques
            const theoricalHours = employees * weeklyHours * weeks;

            // Heures d'absence
            let absenceHours;
            if (inputModeVal === 'heures') {
                absenceHours = parseFloat(document.getElementById('calcAbsAbsenceHours').value);
            } else {
                const absenceDays = parseFloat(document.getElementById('calcAbsAbsenceDays').value);
                const hoursPerDay = weeklyHours / 5;
                absenceHours = absenceDays * hoursPerDay;
            }

            // Détails par type
            let detailsHTML = '';
            if (showDetailsVal) {
                const maladie = parseFloat(document.getElementById('calcAbsMaladie').value) || 0;
                const accident = parseFloat(document.getElementById('calcAbsAccident').value) || 0;
                const congesSansSolde = parseFloat(document.getElementById('calcAbsCongesSansSolde').value) || 0;
                const injustifiees = parseFloat(document.getElementById('calcAbsInjustifiees').value) || 0;
                const autres = parseFloat(document.getElementById('calcAbsAutres').value) || 0;

                const total = maladie + accident + congesSansSolde + injustifiees + autres;

                const details = [
                    { label: 'Maladie ordinaire', value: maladie },
                    { label: 'Accident du travail / Maladie pro.', value: accident },
                    { label: 'Congés sans solde', value: congesSansSolde },
                    { label: 'Absences injustifiées', value: injustifiees },
                    { label: 'Autres', value: autres }
                ];

                details.forEach(item => {
                    if (item.value > 0) {
                        const percentage = total > 0 ? ((item.value / total) * 100).toFixed(1) : 0;
                        const unit = inputModeVal === 'heures' ? 'h' : 'j';
                        detailsHTML += `
                            <div class="calc-absenteisme-result-item">
                                <span class="calc-absenteisme-result-label">${item.label}</span>
                                <span class="calc-absenteisme-result-value">${item.value} ${unit} (${percentage}%)</span>
                            </div>
                        `;
                    }
                });
            }

            // Calcul du taux
            const rate = theoricalHours > 0 ? (absenceHours / theoricalHours) * 100 : 0;

            // Affichage des résultats
            document.getElementById('calcAbsMainRate').textContent = rate.toFixed(2) + '%';
            document.getElementById('calcAbsThericalHours').textContent = theoricalHours.toFixed(0) + ' h';
            document.getElementById('calcAbsTotalAbsence').textContent = absenceHours.toFixed(1) + ' h';
            document.getElementById('calcAbsDisplayEmployees').textContent = employees;

            let periodLabel;
            switch(periodTypeVal) {
                case 'mensuel': periodLabel = 'Mensuel'; break;
                case 'trimestriel': periodLabel = 'Trimestriel'; break;
                case 'annuel': periodLabel = 'Annuel'; break;
                case 'personnalise': periodLabel = document.getElementById('calcAbsCustomDays').value + ' jours'; break;
            }
            document.getElementById('calcAbsDisplayPeriod').textContent = periodLabel;

            // Affichage des détails
            const detailsResults = document.getElementById('calcAbsDetailsResults');
            if (showDetailsVal && detailsHTML) {
                detailsResults.classList.remove('calc-absenteisme-hidden');
                document.getElementById('calcAbsDetailsContent').innerHTML = detailsHTML;
            } else {
                detailsResults.classList.add('calc-absenteisme-hidden');
            }

            // Interprétation
            const interpretation = document.getElementById('calcAbsInterpretation');
            let interpretationText = '';
            let interpretationClass = '';

            if (rate < 3) {
                interpretationClass = 'good';
                interpretationText = '✅ <strong>Taux excellent</strong> - Votre taux d\'absentéisme est très bas, ce qui indique une bonne santé organisationnelle.';
            } else if (rate < 5) {
                interpretationClass = 'good';
                interpretationText = '✅ <strong>Taux bon</strong> - Votre taux d\'absentéisme est dans la moyenne française (environ 4-5%).';
            } else if (rate < 8) {
                interpretationClass = 'warning';
                interpretationText = '⚠️ <strong>Taux à surveiller</strong> - Votre taux d\'absentéisme est légèrement élevé. Il peut être utile d\'identifier les causes principales.';
            } else {
                interpretationClass = 'alert';
                interpretationText = '🔴 <strong>Taux élevé</strong> - Votre taux d\'absentéisme est préoccupant. Il est recommandé de mettre en place des actions correctives et d\'analyser les causes (conditions de travail, climat social, organisation, etc.).';
            }

            interpretation.className = 'calc-absenteisme-interpretation ' + interpretationClass;
            interpretation.innerHTML = interpretationText;

            // Affichage des résultats
            const results = document.getElementById('calcAbsResults');
            results.classList.add('show');

            // Scroll uniquement sur mobile
            if (window.innerWidth < 1024) {
                results.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            }
        });
    }

    // Support pour Elementor Editor
    if (window.elementorFrontend) {
        window.elementorFrontend.hooks.addAction('frontend/element_ready/widget', function() {
            initCalculateurAbsenteisme();
        });
    }
})();
