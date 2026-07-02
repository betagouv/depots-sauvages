<template>
  <div class="fr-tabs__panel fr-tabs__panel--selected" role="tabpanel">
    <div v-if="!selectedProcedure" class="fr-text-center fr-py-5w">
      <span class="fr-icon-arrow-left-line fr-mr-1w" aria-hidden="true"></span>
      Veuillez sélectionner une procédure dans le tableau de bord ou la liste pour afficher ses
      détails.
    </div>

    <div v-else>
      <!-- Stepper/Timeline progress bar -->
      <StepperTimeline :current-step="selectedProcedure.suivi_procedure.etape_en_cours" />


      <div class="fr-grid-row fr-grid-row--gutters">
        <!-- Left Column: Constatation Details -->
        <div class="fr-col-12 fr-col-md-7">
          <!-- 1. General & Contact Card -->
          <div class="premium-box fr-p-3w fr-mb-3w" style="background: white; border-radius: 8px; box-shadow: var(--shadow-md)">
            <h3 class="fr-h6 fr-mb-2w" style="border-bottom: 1px solid var(--border-default-grey); padding-bottom: 0.5rem; color: var(--text-title-blue-france)">
              <span class="fr-icon-user-line fr-mr-1w"></span> Général & Contact
            </h3>
            <div class="fr-grid-row fr-grid-row--gutters">
              <div class="fr-col-6">
                <span class="fr-text--xs fr-mb-0" style="color: var(--text-mention-grey); text-transform: uppercase">Commune</span>
                <p class="fr-text--md fr-mb-1w"><strong>{{ selectedProcedure.commune }}</strong></p>
              </div>
              <div class="fr-col-6">
                <span class="fr-text--xs fr-mb-0" style="color: var(--text-mention-grey); text-transform: uppercase">Agent Constatant</span>
                <p class="fr-text--md fr-mb-1w">{{ selectedProcedure.agent }} ({{ selectedProcedure.constatant_role || 'Rôle non spécifié' }})</p>
              </div>
              <div class="fr-col-6">
                <span class="fr-text--xs fr-mb-0" style="color: var(--text-mention-grey); text-transform: uppercase">Date & Heure</span>
                <p class="fr-text--md fr-mb-1w">{{ formatDate(selectedProcedure.date_constat) }} {{ selectedProcedure.heure_constat ? `à ${selectedProcedure.heure_constat.substring(0, 5)}` : '' }}</p>
              </div>
              <div class="fr-col-6">
                <span class="fr-text--xs fr-mb-0" style="color: var(--text-mention-grey); text-transform: uppercase">N° Procédure</span>
                <p class="fr-text--md fr-mb-1w"><code>#{{ selectedProcedure.id }}</code></p>
              </div>
              <div class="fr-col-12" style="border-top: 1px dashed var(--border-default-grey); padding-top: 1rem">
                <span class="fr-text--xs fr-mb-0" style="color: var(--text-mention-grey); text-transform: uppercase">Contact Collectivité</span>
                <p class="fr-text--sm fr-mb-0">
                  <strong>{{ selectedProcedure.contact_prenom }} {{ selectedProcedure.contact_nom }}</strong>
                  <span v-if="selectedProcedure.contact_email"> | ✉ {{ selectedProcedure.contact_email }}</span>
                  <span v-if="selectedProcedure.contact_telephone"> | 📞 {{ selectedProcedure.contact_telephone }}</span>
                </p>
                <p class="fr-text--xs fr-mt-1v fr-mb-0" style="color: var(--text-mention-grey)">
                  Accompagnement souhaité : <strong>{{ selectedProcedure.accepte_accompagnement ? 'Oui' : 'Non' }}</strong>
                </p>
              </div>
            </div>
          </div>

          <!-- 2. Deposit Details Card -->
          <div class="premium-box fr-p-3w fr-mb-3w" style="background: white; border-radius: 8px; box-shadow: var(--shadow-md)">
            <h3 class="fr-h6 fr-mb-2w" style="border-bottom: 1px solid var(--border-default-grey); padding-bottom: 0.5rem; color: var(--text-title-blue-france)">
              <span class="fr-icon-road-map-line fr-mr-1w"></span> Description du Dépôt
            </h3>
            <div class="fr-grid-row fr-grid-row--gutters">
              <div class="fr-col-6">
                <span class="fr-text--xs fr-mb-0" style="color: var(--text-mention-grey); text-transform: uppercase">Terrain</span>
                <p class="fr-text--md fr-mb-1w">
                  {{ selectedProcedure.nature_terrain.join(', ') || 'N/A' }}
                  <span v-if="selectedProcedure.proprietaire_terrain_prive" class="fr-text--xs" style="color: var(--text-mention-grey)">
                    (Propriétaire privé: {{ selectedProcedure.proprietaire_terrain_prive }})
                  </span>
                </p>
              </div>
              <div class="fr-col-6">
                <span class="fr-text--xs fr-mb-0" style="color: var(--text-mention-grey); text-transform: uppercase">Volume estimé</span>
                <p class="fr-text--md fr-mb-1w"><strong>{{ selectedProcedure.volume_depot || 'Non renseigné' }}</strong></p>
              </div>
              <div class="fr-col-12">
                <span class="fr-text--xs fr-mb-0" style="color: var(--text-mention-grey); text-transform: uppercase">Types de déchets</span>
                <div class="fr-mt-1v" style="display: flex; flex-wrap: wrap; gap: 0.35rem">
                  <span
                    v-for="t in selectedProcedure.types_depot"
                    :key="t"
                    class="fr-tag fr-tag--sm"
                  >
                    {{ t }}
                  </span>
                  <span v-if="!selectedProcedure.types_depot?.length" style="color: var(--text-mention-grey)">N/A</span>
                </div>
              </div>
              <div class="fr-col-12" v-if="selectedProcedure.precisions_depot">
                <span class="fr-text--xs fr-mb-0" style="color: var(--text-mention-grey); text-transform: uppercase">Précisions</span>
                <p class="fr-text--sm fr-mb-1w" style="white-space: pre-wrap">{{ selectedProcedure.precisions_depot }}</p>
              </div>
              <div class="fr-col-12">
                <span class="fr-text--xs fr-mb-0" style="color: var(--text-mention-grey); text-transform: uppercase">Photos disponibles</span>
                <p class="fr-text--md fr-mb-0">
                  <span v-if="selectedProcedure.photo_dispo" class="fr-icon-checkbox-circle-fill" style="color: #22C55E"></span>
                  <span v-else class="fr-icon-close-circle-fill" style="color: #EF4444"></span>
                  {{ selectedProcedure.photo_dispo ? ' Oui' : ' Non' }}
                </p>
              </div>
            </div>
          </div>

          <!-- 3. Author & Clues Card -->
          <div class="premium-box fr-p-3w fr-mb-3w" style="background: white; border-radius: 8px; box-shadow: var(--shadow-md)">
            <h3 class="fr-h6 fr-mb-2w" style="border-bottom: 1px solid var(--border-default-grey); padding-bottom: 0.5rem; color: var(--text-title-blue-france)">
              <span class="fr-icon-user-search-line fr-mr-1w"></span> Auteur Présumé & Indices
            </h3>
            <div class="fr-grid-row fr-grid-row--gutters">
              <div class="fr-col-6">
                <span class="fr-text--xs fr-mb-0" style="color: var(--text-mention-grey); text-transform: uppercase">Auteur identifié</span>
                <p class="fr-text--md fr-mb-1w"><strong>{{ selectedProcedure.auteur_identifie ? 'Oui' : 'Non présumé' }}</strong></p>
              </div>
              <div class="fr-col-6" v-if="selectedProcedure.statut_auteur">
                <span class="fr-text--xs fr-mb-0" style="color: var(--text-mention-grey); text-transform: uppercase">Statut auteur</span>
                <p class="fr-text--md fr-mb-1w">{{ selectedProcedure.statut_auteur }}</p>
              </div>
              <div class="fr-col-12" v-if="selectedProcedure.auteur_nom || selectedProcedure.auteur_prenom">
                <span class="fr-text--xs fr-mb-0" style="color: var(--text-mention-grey); text-transform: uppercase">Identité auteur</span>
                <p class="fr-text--md fr-mb-1w">
                  <strong>{{ selectedProcedure.auteur_civilite }} {{ selectedProcedure.auteur_prenom }} {{ selectedProcedure.auteur_nom }}</strong>
                  <span v-if="selectedProcedure.auteur_siret"> (SIRET: {{ selectedProcedure.auteur_siret }})</span>
                  <span v-if="selectedProcedure.entreprise_francaise !== null" class="fr-text--xs" style="color: var(--text-mention-grey)">
                    - {{ selectedProcedure.entreprise_francaise ? 'Entreprise française' : 'Entreprise étrangère' }}
                  </span>
                </p>
              </div>
              <div class="fr-col-12" v-if="selectedProcedure.auteur_adresse">
                <span class="fr-text--xs fr-mb-0" style="color: var(--text-mention-grey); text-transform: uppercase">Adresse auteur</span>
                <p class="fr-text--sm fr-mb-1w">{{ selectedProcedure.auteur_adresse }}</p>
              </div>
              <div class="fr-col-12" style="border-top: 1px dashed var(--border-default-grey); padding-top: 1rem">
                <span class="fr-text--xs fr-mb-0" style="color: var(--text-mention-grey); text-transform: uppercase">Indices trouvés sur place</span>
                <div class="fr-mt-1v fr-mb-1w" style="display: flex; flex-wrap: wrap; gap: 0.35rem">
                  <span
                    v-for="idx in selectedProcedure.indices_disponibles"
                    :key="idx"
                    class="fr-tag fr-tag--sm"
                  >
                    {{ idx }}
                  </span>
                  <span v-if="!selectedProcedure.indices_disponibles?.length" style="color: var(--text-mention-grey)">Aucun indice</span>
                </div>
                <p class="fr-text--sm fr-mb-0" v-if="selectedProcedure.precisions_indices" style="white-space: pre-wrap">
                  {{ selectedProcedure.precisions_indices }}
                </p>
              </div>
            </div>
          </div>

          <!-- 4. Prejudice Estimations Card -->
          <div class="premium-box fr-p-3w fr-mb-3w" style="background: white; border-radius: 8px; box-shadow: var(--shadow-md)">
            <h3 class="fr-h6 fr-mb-2w" style="border-bottom: 1px solid var(--border-default-grey); padding-bottom: 0.5rem; color: var(--text-title-blue-france)">
              <span class="fr-icon-money-euro-box-line fr-mr-1w"></span> Évaluation du Préjudice Financier
            </h3>
            <div class="fr-grid-row fr-grid-row--gutters">
              <!-- Row 1: State of complaint & total amount side by side -->
              <div class="fr-col-6">
                <span class="fr-text--xs fr-mb-0" style="color: var(--text-mention-grey); text-transform: uppercase">État de la plainte</span>
                <p class="fr-text--md fr-mb-1w"><strong>{{ selectedProcedure.plainte_etat || 'Aucune plainte' }}</strong></p>
              </div>
              <div class="fr-col-6" style="text-align: right">
                <span class="fr-text--xs fr-mb-0" style="color: var(--text-mention-grey); text-transform: uppercase">Montant total du préjudice</span>
                <p class="fr-h4 fr-mb-0" :style="{ color: selectedProcedure.prejudice_montant ? '#EF4444' : 'var(--text-mention-grey)' }">
                  {{ selectedProcedure.prejudice_montant !== null && selectedProcedure.prejudice_montant !== undefined ? `${selectedProcedure.prejudice_montant.toLocaleString('fr-FR')} €` : (['Déposée', 'Sera déposée'].includes(selectedProcedure.plainte_etat) ? 'Calcul en cours' : '0 €') }}
                </p>
              </div>

              <!-- Row 2: Calculation Details -->
              <div class="fr-col-12" style="border-top: 1px dashed var(--border-default-grey); padding-top: 1rem">
                <div class="fr-grid-row fr-grid-row--gutters fr-text--xs">
                  <div class="fr-col-4">
                    <span style="color: var(--text-mention-grey)">Agents</span>
                    <p class="fr-text--sm fr-mb-0 font-weight-bold">{{ selectedProcedure.prejudice_nombre_personnes || 0 }}</p>
                  </div>
                  <div class="fr-col-4">
                    <span style="color: var(--text-mention-grey)">Heures</span>
                    <p class="fr-text--sm fr-mb-0 font-weight-bold">{{ selectedProcedure.prejudice_nombre_heures || 0 }}</p>
                  </div>
                  <div class="fr-col-4">
                    <span style="color: var(--text-mention-grey)">Véhicules</span>
                    <p class="fr-text--sm fr-mb-0 font-weight-bold">{{ selectedProcedure.prejudice_nombre_vehicules || 0 }}</p>
                  </div>
                  <div class="fr-col-4">
                    <span style="color: var(--text-mention-grey)">Kilomètres</span>
                    <p class="fr-text--sm fr-mb-0 font-weight-bold">{{ selectedProcedure.prejudice_kilometrage || 0 }}</p>
                  </div>
                  <div class="fr-col-8">
                    <span style="color: var(--text-mention-grey)">Autres coûts</span>
                    <p class="fr-text--sm fr-mb-0 font-weight-bold">{{ selectedProcedure.prejudice_autres_couts ? `${selectedProcedure.prejudice_autres_couts} €` : '0 €' }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 5. Documents Section -->
          <div class="premium-box fr-p-3w" style="background: white; border-radius: 8px; box-shadow: var(--shadow-md)">
            <h3 class="fr-h6 fr-mb-2w" style="border-bottom: 1px solid var(--border-default-grey); padding-bottom: 0.5rem; color: var(--text-title-blue-france)">
              <span class="fr-icon-file-pdf-line fr-mr-1w"></span> Documents de la Procédure
            </h3>
            <div style="display: flex; flex-direction: column; gap: 1rem">
              <!-- Rapport de constatation -->
              <div class="fr-p-1w" style="display: flex; justify-content: space-between; align-items: center; background: var(--background-alt-grey); border-radius: 6px">
                <div>
                  <p class="fr-text--sm fr-mb-0"><strong>Rapport de constatation</strong></p>
                  <p class="fr-text--xs fr-mb-0" style="color: var(--text-mention-grey)">
                    Généré le : {{ formatDate(selectedProcedure.doc_constat_generated_at) }}
                  </p>
                </div>
                <a
                  v-if="selectedProcedure.doc_constat_generated_at"
                  :href="`/api/constatations/${selectedProcedure.id}/documents/doc_constat/`"
                  target="_blank"
                  class="fr-btn fr-btn--sm fr-btn--secondary fr-icon-download-line"
                >
                  Télécharger
                </a>
                <span v-else class="fr-text--xs" style="color: var(--text-mention-grey)">Non généré</span>
              </div>

              <!-- Lettre d'information -->
              <div class="fr-p-1w" style="display: flex; justify-content: space-between; align-items: center; background: var(--background-alt-grey); border-radius: 6px">
                <div>
                  <p class="fr-text--sm fr-mb-0"><strong>Lettre d'information</strong></p>
                  <p class="fr-text--xs fr-mb-0" style="color: var(--text-mention-grey)">
                    Généré le : {{ formatDate(selectedProcedure.lettre_info_generated_at) }}
                  </p>
                </div>
                <a
                  v-if="selectedProcedure.lettre_info_generated_at"
                  :href="`/api/constatations/${selectedProcedure.id}/documents/lettre_info/`"
                  target="_blank"
                  class="fr-btn fr-btn--sm fr-btn--secondary fr-icon-download-line"
                >
                  Télécharger
                </a>
                <span v-else class="fr-text--xs" style="color: var(--text-mention-grey)">Non générée</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Right Column: Suivi de Procédure Checklist & Pilotage -->
        <div class="fr-col-12 fr-col-md-5">
          <!-- Assignation & Notes -->
          <div class="premium-box fr-p-3w fr-mb-3w" style="background: white; border-radius: 8px; box-shadow: var(--shadow-md); border-top: 4px solid var(--border-active-blue-france)">
            <h3 class="fr-h6 fr-mb-2w" style="color: var(--text-title-blue-france)">
              <span class="fr-icon-user-setting-line fr-mr-1w"></span> Pilotage dossier
            </h3>
            <!-- Officer Assignee -->
            <div class="fr-select-group fr-mb-2w">
              <label class="fr-label fr-text--xs" for="assignee-select">Chargé de déploiement</label>
              <select
                id="assignee-select"
                class="fr-select"
                :value="selectedProcedure.suivi_procedure.charge_deploiement"
                @change="
                  store.assignCharge(
                    selectedProcedure.id,
                    ($event.target as HTMLSelectElement).value
                  )
                "
              >
                <option v-for="name in store.assignees" :key="name" :value="name">
                  {{ name }}
                </option>
              </select>
              <p
                v-if="selectedProcedure.suivi_procedure.date_assigned"
                class="fr-text--xs fr-mt-1w fr-mb-0"
                style="color: var(--text-mention-grey)"
              >
                Assigné le {{ formatDate(selectedProcedure.suivi_procedure.date_assigned) }}
              </p>
            </div>

            <!-- Internal Notes -->
            <div class="fr-input-group fr-mb-0">
              <label class="fr-label fr-text--xs" for="internal-notes">Notes de suivi & Observations</label>
              <textarea
                id="internal-notes"
                class="fr-input"
                placeholder="Relance, appels, blocages..."
                style="min-height: 100px"
                :value="selectedProcedure.suivi_procedure.observations_internes"
                @change="
                  store.updateNotes(
                    selectedProcedure.id,
                    ($event.target as HTMLTextAreaElement).value
                  )
                "
              ></textarea>
            </div>
          </div>

          <!-- Chronological Step-by-Step Followup -->
          <div class="premium-box fr-p-3w" style="background: white; border-radius: 8px; box-shadow: var(--shadow-md)">
            <h3 class="fr-h6 fr-mb-3w" style="border-bottom: 1px solid var(--border-default-grey); padding-bottom: 0.5rem; color: var(--text-title-blue-france)">
              <span class="fr-icon-survey-line fr-mr-1w"></span> Actions du Suivi
            </h3>

            <!-- ÉTAPE 1: Pièces jointes -->
            <div class="fr-mb-3w" style="border-left: 2px solid #22C55E; padding-left: 1rem">
              <h4 class="fr-text--sm fr-mb-1w" style="font-weight: 700; color: #15803D">Étape 1 : Constitution du dossier</h4>
              <div style="display: flex; flex-direction: column; gap: 0.5rem">
                <!-- preuves_fournies -->
                <div class="premium-action-item fr-p-1v" style="display: flex; align-items: center">
                  <span class="fr-mr-1w" :class="selectedProcedure.suivi_procedure.preuves_fournies ? 'fr-icon-checkbox-circle-fill' : 'fr-icon-checkbox-blank-line'" :style="{ color: selectedProcedure.suivi_procedure.preuves_fournies ? '#22C55E' : '#9CA3AF' }"></span>
                  <span class="fr-text--xs">Éléments de preuve joints</span>
                </div>
                <!-- constatation_signee -->
                <div class="premium-action-item fr-p-1v" style="display: flex; align-items: center">
                  <span class="fr-mr-1w" :class="selectedProcedure.suivi_procedure.constatation_signee ? 'fr-icon-checkbox-circle-fill' : 'fr-icon-checkbox-blank-line'" :style="{ color: selectedProcedure.suivi_procedure.constatation_signee ? '#22C55E' : '#9CA3AF' }"></span>
                  <span class="fr-text--xs">Rapport de constatation signé</span>
                </div>
                <!-- lettre_signe -->
                <div class="premium-action-item fr-p-1v" style="display: flex; align-items: center">
                  <span class="fr-mr-1w" :class="selectedProcedure.suivi_procedure.lettre_signe ? 'fr-icon-checkbox-circle-fill' : 'fr-icon-checkbox-blank-line'" :style="{ color: selectedProcedure.suivi_procedure.lettre_signe ? '#22C55E' : '#9CA3AF' }"></span>
                  <span class="fr-text--xs">Lettre d'information signée</span>
                </div>
                <!-- identification_reussie -->
                <div class="premium-action-item fr-p-1v" style="display: flex; align-items: center">
                  <span class="fr-mr-1w" :class="selectedProcedure.suivi_procedure.identification_reussie === true ? 'fr-icon-checkbox-circle-fill' : selectedProcedure.suivi_procedure.identification_reussie === false ? 'fr-icon-close-circle-fill' : 'fr-icon-checkbox-blank-line'" :style="{ color: selectedProcedure.suivi_procedure.identification_reussie === true ? '#22C55E' : selectedProcedure.suivi_procedure.identification_reussie === false ? '#EF4444' : '#9CA3AF' }"></span>
                  <span class="fr-text--xs">Identification auteur : <strong>{{ getAuteurIdentifieText(selectedProcedure.suivi_procedure.identification_reussie) }}</strong></span>
                </div>
              </div>
            </div>

            <!-- ÉTAPE 2: Notification -->
            <div class="fr-mb-3w" :style="{ borderLeft: '2px solid ' + (selectedProcedure.suivi_procedure.etape_en_cours >= 2 ? '#22C55E' : '#9CA3AF'), paddingLeft: '1rem' }">
              <h4 class="fr-text--sm fr-mb-1w" style="font-weight: 700" :style="{ color: selectedProcedure.suivi_procedure.etape_en_cours >= 2 ? '#15803D' : '#4B5563' }">Étape 2 : Notification à l'auteur</h4>
              <div style="display: flex; flex-direction: column; gap: 0.5rem">
                <!-- lettre_envoyee & date -->
                <div style="display: flex; align-items: center; justify-content: space-between">
                  <label class="fr-text--xs fr-mb-0" style="display: flex; align-items: center; gap: 0.5rem">
                    <input type="checkbox" :checked="selectedProcedure.suivi_procedure.lettre_envoyee" disabled />
                    Lettre d'information envoyée
                  </label>
                  <input
                    v-if="selectedProcedure.suivi_procedure.lettre_envoyee"
                    type="date"
                    class="fr-input fr-input--sm"
                    style="width: 120px; padding: 0.2rem"
                    :value="selectedProcedure.suivi_procedure.lettre_envoyee_date"
                    disabled
                  />
                </div>
                <!-- ar_recu, ar_statut & date -->
                <div style="display: flex; align-items: center; justify-content: space-between">
                  <label class="fr-text--xs fr-mb-0" style="display: flex; align-items: center; gap: 0.5rem">
                    <input type="checkbox" :checked="selectedProcedure.suivi_procedure.ar_recu" disabled />
                    Accusé de réception (AR) reçu
                  </label>
                </div>
                <div v-if="selectedProcedure.suivi_procedure.ar_recu" style="display: flex; gap: 0.5rem; margin-left: 1.25rem">
                  <input
                    type="text"
                    class="fr-input fr-input--sm"
                    placeholder="Statut AR (ex: Distribué)"
                    :value="selectedProcedure.suivi_procedure.ar_statut"
                    disabled
                    style="flex: 1; padding: 0.2rem"
                  />
                  <input
                    type="date"
                    class="fr-input fr-input--sm"
                    :value="selectedProcedure.suivi_procedure.ar_presentation_date"
                    disabled
                    style="width: 120px; padding: 0.2rem"
                  />
                </div>
                <!-- copie_archives -->
                <label class="fr-text--xs fr-mb-0" style="display: flex; align-items: center; gap: 0.5rem">
                  <input type="checkbox" :checked="selectedProcedure.suivi_procedure.copie_archives" disabled />
                  Copie archivée dans le dossier
                </label>
              </div>
            </div>

            <!-- ÉTAPE 3: Décision de poursuite -->
            <div class="fr-mb-3w" :style="{ borderLeft: '2px solid ' + (selectedProcedure.suivi_procedure.etape_en_cours >= 3 ? '#22C55E' : '#9CA3AF'), paddingLeft: '1rem' }">
              <h4 class="fr-text--sm fr-mb-1w" style="font-weight: 700" :style="{ color: selectedProcedure.suivi_procedure.etape_en_cours >= 3 ? '#15803D' : '#4B5563' }">Étape 3 : Décision de poursuite</h4>
              <div class="fr-select-group fr-mb-0">
                <select
                  class="fr-select fr-select--sm"
                  :value="selectedProcedure.suivi_procedure.decision_poursuite"
                  disabled
                  style="padding: 0.25rem"
                >
                  <option value="">-- Sélectionner la décision --</option>
                  <option value="sanction">Sanction administrative</option>
                  <option value="abandon">Abandon de la procédure</option>
                  <option value="recherche_adresse">Recherche d'adresse en cours</option>
                </select>
              </div>
            </div>

            <!-- ÉTAPE 4: Exécution de la décision -->
            <div class="fr-mb-3w" :style="{ borderLeft: '2px solid ' + (selectedProcedure.suivi_procedure.etape_en_cours >= 4 ? '#22C55E' : '#9CA3AF'), paddingLeft: '1rem' }">
              <h4 class="fr-text--sm fr-mb-1w" style="font-weight: 700" :style="{ color: selectedProcedure.suivi_procedure.etape_en_cours >= 4 ? '#15803D' : '#4B5563' }">Étape 4 : Exécution de la décision</h4>
              
              <!-- Cas : Sanction -->
              <div v-if="selectedProcedure.suivi_procedure.decision_poursuite === 'sanction'" style="display: flex; flex-direction: column; gap: 0.5rem">
                <div style="display: flex; align-items: center; justify-content: space-between">
                  <label class="fr-text--xs fr-mb-0" style="display: flex; align-items: center; gap: 0.5rem">
                    <input type="checkbox" :checked="selectedProcedure.suivi_procedure.montant_fixe" disabled />
                    Montant de l'amende fixé
                  </label>
                  <input
                    v-if="selectedProcedure.suivi_procedure.montant_fixe"
                    type="number"
                    step="0.01"
                    class="fr-input fr-input--sm"
                    style="width: 100px; padding: 0.2rem"
                    placeholder="Montant €"
                    :value="selectedProcedure.suivi_procedure.montant_amende"
                    disabled
                  />
                </div>
                <label class="fr-text--xs fr-mb-0" style="display: flex; align-items: center; gap: 0.5rem">
                  <input type="checkbox" :checked="selectedProcedure.suivi_procedure.arrete_redige" disabled />
                  Arrêté de sanction rédigé
                </label>
                <label class="fr-text--xs fr-mb-0" style="display: flex; align-items: center; gap: 0.5rem">
                  <input type="checkbox" :checked="selectedProcedure.suivi_procedure.titre_recette_emis" disabled />
                  Titre de recette émis au Trésor Public
                </label>
                <label class="fr-text--xs fr-mb-0" style="display: flex; align-items: center; gap: 0.5rem">
                  <input type="checkbox" :checked="selectedProcedure.suivi_procedure.notification_sanction_envoyee" disabled />
                  Notification de sanction envoyée à l'auteur
                </label>
              </div>

              <!-- Cas : Abandon -->
              <div v-else-if="selectedProcedure.suivi_procedure.decision_poursuite === 'abandon'" style="display: flex; flex-direction: column; gap: 0.5rem">
                <div>
                  <label class="fr-label fr-text--xs fr-mb-1v" for="motif-abandon-select">Motif d'abandon</label>
                  <select
                    id="motif-abandon-select"
                    class="fr-select fr-select--sm"
                    :value="selectedProcedure.suivi_procedure.motif_abandon"
                    disabled
                    style="padding: 0.25rem"
                  >
                    <option value="">-- Sélectionner le motif --</option>
                    <option value="Auteur introuvable (NPAI)">Auteur introuvable (NPAI)</option>
                    <option value="Dépôt sans gravité">Dépôt sans gravité / Mineur</option>
                    <option value="Régularisation immédiate">Régularisation spontanée immédiate</option>
                    <option value="Autre">Autre motif</option>
                  </select>
                </div>
                <label class="fr-text--xs fr-mb-0" style="display: flex; align-items: center; gap: 0.5rem">
                  <input type="checkbox" :checked="selectedProcedure.suivi_procedure.souhaite_notifier_abandon" disabled />
                  Notifier l'abandon à l'auteur
                </label>
                <label v-if="selectedProcedure.suivi_procedure.souhaite_notifier_abandon" class="fr-text--xs fr-mb-0" style="display: flex; align-items: center; gap: 0.5rem">
                  <input type="checkbox" :checked="selectedProcedure.suivi_procedure.notification_abandon_envoyee" disabled />
                  Notification d'abandon envoyée
                </label>
              </div>

              <div v-else class="fr-text--xs" style="color: var(--text-mention-grey)">
                Sélectionnez d'abord une décision d'abandon ou de sanction à l'étape 3.
              </div>
            </div>

            <!-- ÉTAPE 5: Clôture & Recouvrement -->
            <div class="fr-mb-0" :style="{ borderLeft: '2px solid ' + (selectedProcedure.suivi_procedure.etape_en_cours >= 5 ? '#22C55E' : '#9CA3AF'), paddingLeft: '1rem' }">
              <h4 class="fr-text--sm fr-mb-1w" style="font-weight: 700" :style="{ color: selectedProcedure.suivi_procedure.etape_en_cours >= 5 ? '#15803D' : '#4B5563' }">Étape 5 : Clôture & Recouvrement</h4>
              <div style="display: flex; flex-direction: column; gap: 0.5rem">
                <!-- Nettoyage fait -->
                <div style="display: flex; align-items: center; justify-content: space-between">
                  <label class="fr-text--xs fr-mb-0" style="display: flex; align-items: center; gap: 0.5rem">
                    <input type="checkbox" :checked="selectedProcedure.suivi_procedure.nettoyage_fait" disabled />
                    Nettoyage du dépôt effectué
                  </label>
                  <input
                    v-if="selectedProcedure.suivi_procedure.nettoyage_fait"
                    type="text"
                    class="fr-input fr-input--sm"
                    style="width: 120px; padding: 0.2rem"
                    placeholder="Par (ex: Auteur)"
                    :value="selectedProcedure.suivi_procedure.nettoyage_par"
                    disabled
                  />
                </div>
                <!-- Sanction-specific closing steps -->
                <div v-if="selectedProcedure.suivi_procedure.decision_poursuite === 'sanction'" style="display: flex; flex-direction: column; gap: 0.5rem">
                  <label class="fr-text--xs fr-mb-0" style="display: flex; align-items: center; gap: 0.5rem">
                    <input type="checkbox" :checked="selectedProcedure.suivi_procedure.titre_recette_confirme" disabled />
                    Titre de recette confirmed par le Trésor
                  </label>
                  <div style="display: flex; align-items: center; justify-content: space-between">
                    <label class="fr-text--xs fr-mb-0" style="display: flex; align-items: center; gap: 0.5rem">
                      <input type="checkbox" :checked="selectedProcedure.suivi_procedure.montant_recouvre" disabled />
                      Amende recouvrée
                    </label>
                    <input
                      v-if="selectedProcedure.suivi_procedure.montant_recouvre"
                      type="date"
                      class="fr-input fr-input--sm"
                      style="width: 120px; padding: 0.2rem"
                      :value="selectedProcedure.suivi_procedure.date_recouvrement_effective"
                      disabled
                    />
                  </div>
                </div>
                <!-- dossier_archive -->
                <label class="fr-text--xs fr-mb-0" style="display: flex; align-items: center; gap: 0.5rem">
                  <input type="checkbox" :checked="selectedProcedure.suivi_procedure.dossier_archive" disabled />
                  Dossier clos et archivé
                </label>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useBackofficeStore } from '@/stores/backoffice'
import { formatDate, getAuteurIdentifieText, getStepLabel } from '@/utils/backoffice'
import { computed } from 'vue'

import StepperTimeline from '@/components/StepperTimeline.vue'

const store = useBackofficeStore()

const props = defineProps<{
  selectedProcedureId: number | null
}>()

const selectedProcedure = computed(() => {
  if (!props.selectedProcedureId) return null
  return store.getProcedureById(props.selectedProcedureId)
})


const saveSuivi = () => {
  if (selectedProcedure.value) {
    store.saveSuivi(selectedProcedure.value.id)
  }
}
</script>

<style scoped>
.premium-box {
  background-color: #ffffff;
  border: 1px solid var(--border-default-grey);
}
.font-weight-bold {
  font-weight: 700;
}
.premium-action-item {
  transition: background-color 0.2s ease;
  border-radius: 4px;
}
.premium-action-item:hover {
  background-color: var(--background-alt-grey-hover);
}
</style>
