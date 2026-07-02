<template>
  <div class="fr-container fr-py-5w">
    <!-- Header -->
    <div class="fr-grid-row fr-grid-row--middle fr-mb-4w">
      <div class="fr-col">
        <h1
          class="fr-h1"
          style="margin-bottom: 0.5rem; display: flex; align-items: center; gap: 0.75rem"
        >
          <span class="fr-icon-settings-5-line fr-text-title-blue-france" aria-hidden="true"></span>
          Back-office de Pilotage
        </h1>
        <p class="fr-text--lead" style="margin-bottom: 0">
          Gestion et suivi opérationnel des procédures administratives collectives.
        </p>
      </div>
    </div>

    <!-- Main Navigation Tabs -->
    <div class="fr-tabs" style="box-shadow: none">
      <ul class="fr-tabs__list" role="tablist">
        <li role="presentation">
          <button
            class="fr-tabs__tab"
            :aria-selected="currentTab === 'dashboard'"
            role="tab"
            @click="currentTab = 'dashboard'"
          >
            <span class="fr-icon-dashboard-line fr-mr-1w" aria-hidden="true"></span>
            Tableau de bord
          </button>
        </li>
        <li role="presentation">
          <button
            class="fr-tabs__tab"
            :aria-selected="currentTab === 'list'"
            role="tab"
            @click="currentTab = 'list'"
          >
            <span class="fr-icon-list-unordered fr-mr-1w" aria-hidden="true"></span>
            Procédures
          </button>
        </li>
        <li role="presentation">
          <button
            class="fr-tabs__tab"
            :aria-selected="currentTab === 'detail'"
            role="tab"
            @click="currentTab = 'detail'"
          >
            <span class="fr-icon-file-text-line fr-mr-1w" aria-hidden="true"></span>
            Détail procédure {{ selectedProcedureId ? `#${selectedProcedureId}` : '' }}
          </button>
        </li>
        <li role="presentation">
          <button
            class="fr-tabs__tab"
            :aria-selected="currentTab === 'stats'"
            role="tab"
            @click="currentTab = 'stats'"
          >
            <span class="fr-icon-line-chart-line fr-mr-1w" aria-hidden="true"></span>
            Statistiques
          </button>
        </li>
      </ul>

      <!-- ==================================================== -->
      <!-- TAB 1: DASHBOARD                                     -->
      <!-- ==================================================== -->
      <div
        v-if="currentTab === 'dashboard'"
        class="fr-tabs__panel fr-tabs__panel--selected"
        role="tabpanel"
      >
        <!-- KPI Cards Grid -->
        <div class="bo-dashboard-grid">
          <div class="bo-kpi-card">
            <div class="bo-kpi-val">{{ store.stats.totalActive }}</div>
            <div class="bo-kpi-lbl">Procédures actives</div>
          </div>
          <div class="bo-kpi-card">
            <div class="bo-kpi-val" style="color: #d97706">{{ store.stats.actionRequired }}</div>
            <div class="bo-kpi-lbl">Action requise</div>
          </div>
          <div class="bo-kpi-card">
            <div class="bo-kpi-val" style="color: #2563eb">{{ store.stats.arWaiting }}</div>
            <div class="bo-kpi-lbl">AR en attente</div>
          </div>
          <div class="bo-kpi-card">
            <div class="bo-kpi-val" style="color: #7c3aed">{{ store.stats.decisionToTake }}</div>
            <div class="bo-kpi-lbl">Décision à prendre</div>
          </div>
          <div class="bo-kpi-card">
            <div class="bo-kpi-val" style="color: #059669">{{ store.stats.closedThisMonth }}</div>
            <div class="bo-kpi-lbl">Clôturées ce mois</div>
          </div>
        </div>

        <!-- Section: Actions requises -->
        <div class="fr-mb-3w">
          <h2 class="fr-h4" style="display: flex; align-items: center; gap: 0.5rem">
            <span
              class="fr-icon-warning-line style-icon"
              style="color: #d97706"
              aria-hidden="true"
            ></span>
            Procédures nécessitant une action prioritaire
          </h2>
          <div class="bo-table-container">
            <table class="bo-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Commune</th>
                  <th>Utilisateur</th>
                  <th>Étape</th>
                  <th>Statut</th>
                  <th>Depuis</th>
                  <th>Chargé Dépl.</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="proc in store.proceduresRequiringAction" :key="proc.id">
                  <td>
                    <code>#{{ proc.id }}</code>
                  </td>
                  <td>
                    <strong>{{ proc.commune }}</strong>
                  </td>
                  <td>
                    <a :href="'mailto:' + proc.user_email" style="font-size: 0.8rem">{{
                      proc.user_email
                    }}</a>
                  </td>
                  <td>
                    <span class="bo-dot bo-dot--active fr-mr-1v"></span>
                    {{ proc.suivi_procedure.etape_en_cours }}
                  </td>
                  <td>
                    <span :class="getBadgeClass(getProcedureStatut(proc))">
                      {{ getProcedureStatut(proc) }}
                    </span>
                  </td>
                  <td>{{ getDepuisText(proc.date_constat) }}</td>
                  <td>
                    <span
                      v-if="proc.suivi_procedure.charge_deploiement === 'Non assigné'"
                      style="color: #d97706; font-weight: 700"
                    >
                      ⚠ Non assigné
                    </span>
                    <span v-else>{{ proc.suivi_procedure.charge_deploiement }}</span>
                  </td>
                  <td>
                    <button class="fr-btn fr-btn--sm" @click="viewDetail(proc.id)">Gérer</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- ==================================================== -->
      <!-- TAB 2: PROCEDURES LIST                               -->
      <!-- ==================================================== -->
      <div
        v-if="currentTab === 'list'"
        class="fr-tabs__panel fr-tabs__panel--selected"
        role="tabpanel"
      >
        <!-- Filter Bar -->
        <div class="bo-filter-bar">
          <div class="bo-filter-group">
            <span class="bo-filter-label">Étape :</span>
            <select
              v-model="filters.etape"
              class="fr-select"
              style="width: auto; padding-right: 2rem"
            >
              <option value="Tous">Tous</option>
              <option :value="1">1 (Pièces)</option>
              <option :value="2">2 (Notification)</option>
              <option :value="3">3 (Décision)</option>
              <option :value="4">4 (Exécution)</option>
              <option :value="5">5 (Clôture)</option>
            </select>
          </div>

          <div class="bo-filter-group">
            <span class="bo-filter-label">Statut :</span>
            <select
              v-model="filters.statut"
              class="fr-select"
              style="width: auto; padding-right: 2rem"
            >
              <option value="Tous">Tous</option>
              <option value="Pièces incomplètes">Pièces incomplètes</option>
              <option value="Auteur non identifié">Auteur non identifié</option>
              <option value="Décision à prendre">Décision à prendre</option>
              <option value="Lettre à envoyer">Lettre à envoyer</option>
            </select>
          </div>

          <div class="bo-filter-group">
            <span class="bo-filter-label">Chargé :</span>
            <select
              v-model="filters.charge"
              class="fr-select"
              style="width: auto; padding-right: 2rem"
            >
              <option value="Tous">Tous</option>
              <option v-for="name in store.assignees" :key="name" :value="name">{{ name }}</option>
            </select>
          </div>

          <div class="bo-filter-group">
            <span class="bo-filter-label">Anomalie :</span>
            <select
              v-model="filters.anomalie"
              class="fr-select"
              style="width: auto; padding-right: 2rem"
            >
              <option value="Toutes">Toutes</option>
              <option value="Avec">Avec anomalie ⚠</option>
              <option value="Sans">Sans anomalie</option>
            </select>
          </div>

          <div class="bo-filter-group" style="flex-grow: 1">
            <input
              v-model="filters.search"
              type="text"
              class="fr-input"
              placeholder="🔍 Rechercher une commune ou agent..."
              style="width: 100%"
            />
          </div>
        </div>

        <!-- Procedures Grid Table -->
        <div class="bo-table-container">
          <table class="bo-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Commune</th>
                <th>Agent</th>
                <th>Date Constat</th>
                <th>Statut</th>
                <th>Chargé</th>
                <th>Anomalies / Alertes</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="proc in filteredProcedures" :key="proc.id">
                <td>
                  <code>#{{ proc.id }}</code>
                </td>
                <td>
                  <strong>{{ proc.commune }}</strong>
                </td>
                <td>{{ proc.agent }}</td>
                <td>{{ formatDate(proc.date_constat) }}</td>
                <td>
                  <span :class="getBadgeClass(getProcedureStatut(proc))">
                    ● Étape {{ proc.suivi_procedure.etape_en_cours }} :
                    {{ getProcedureStatut(proc) }}
                  </span>
                </td>
                <td>{{ proc.suivi_procedure.charge_deploiement }}</td>
                <td>
                  <span
                    v-if="proc.suivi_procedure.anomalie"
                    class="fr-text--xs"
                    style="color: #dc2626; font-weight: 700"
                  >
                    ⚠ {{ proc.suivi_procedure.anomalie }}
                  </span>
                  <span v-else class="fr-text--xs" style="color: #9ca3af">Aucune</span>
                </td>
                <td>
                  <button class="fr-btn fr-btn--sm fr-btn--secondary" @click="viewDetail(proc.id)">
                    Consulter
                  </button>
                </td>
              </tr>
              <tr v-if="filteredProcedures.length === 0">
                <td
                  colspan="8"
                  class="fr-text-center fr-py-3w"
                  style="color: var(--text-mention-grey)"
                >
                  Aucune procédure ne correspond aux filtres appliqués.
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- ==================================================== -->
      <!-- TAB 3: PROCEDURE DETAIL                              -->
      <!-- ==================================================== -->
      <div
        v-if="currentTab === 'detail'"
        class="fr-tabs__panel fr-tabs__panel--selected"
        role="tabpanel"
      >
        <div v-if="!selectedProcedure" class="fr-text-center fr-py-5w">
          <span class="fr-icon-arrow-left-line fr-mr-1w" aria-hidden="true"></span>
          Veuillez sélectionner une procédure dans le tableau de bord ou la liste pour afficher ses
          détails.
        </div>

        <div v-else>
          <!-- Stepper/Timeline progress bar -->
          <div class="bo-stepper">
            <div
              v-for="step in 5"
              :key="step"
              class="bo-step"
              :class="{
                'bo-step--completed': selectedProcedure.suivi_procedure.etape_en_cours > step,
                'bo-step--active': selectedProcedure.suivi_procedure.etape_en_cours === step,
              }"
            >
              <div class="bo-step-num">{{ step }}</div>
              <div class="bo-step-lbl">{{ getStepLabel(step) }}</div>
            </div>
          </div>

          <div class="fr-grid-row fr-grid-row--gutters">
            <!-- Left Info Panel -->
            <div class="fr-col-12 fr-col-md-7">
              <!-- Constatation Overview Card -->
              <div class="premium-box fr-p-3w fr-mb-3w" style="background: white">
                <h3
                  class="fr-h5"
                  style="
                    border-bottom: 1px solid var(--border-default-grey);
                    padding-bottom: 0.5rem;
                  "
                >
                  Constatation
                </h3>
                <div class="fr-grid-row fr-grid-row--gutters">
                  <div class="fr-col-6">
                    <p
                      class="fr-text--xs fr-mb-1v"
                      style="color: var(--text-mention-grey); text-transform: uppercase"
                    >
                      Commune
                    </p>
                    <p class="fr-text--md">
                      <strong>{{ selectedProcedure.commune }}</strong>
                    </p>
                  </div>
                  <div class="fr-col-6">
                    <p
                      class="fr-text--xs fr-mb-1v"
                      style="color: var(--text-mention-grey); text-transform: uppercase"
                    >
                      Agent Constatant
                    </p>
                    <p class="fr-text--md">{{ selectedProcedure.agent }}</p>
                  </div>
                  <div class="fr-col-6">
                    <p
                      class="fr-text--xs fr-mb-1v"
                      style="color: var(--text-mention-grey); text-transform: uppercase"
                    >
                      Rôle
                    </p>
                    <p class="fr-text--md">{{ selectedProcedure.constatant_role }}</p>
                  </div>
                  <div class="fr-col-6">
                    <p
                      class="fr-text--xs fr-mb-1v"
                      style="color: var(--text-mention-grey); text-transform: uppercase"
                    >
                      Date du Constat
                    </p>
                    <p class="fr-text--md">{{ formatDate(selectedProcedure.date_constat) }}</p>
                  </div>
                  <div class="fr-col-6">
                    <p
                      class="fr-text--xs fr-mb-1v"
                      style="color: var(--text-mention-grey); text-transform: uppercase"
                    >
                      N° Procédure
                    </p>
                    <p class="fr-text--md">
                      <code>{{ selectedProcedure.id }}</code>
                    </p>
                  </div>
                  <div class="fr-col-6">
                    <p
                      class="fr-text--xs fr-mb-1v"
                      style="color: var(--text-mention-grey); text-transform: uppercase"
                    >
                      Type de Terrain
                    </p>
                    <p class="fr-text--md">{{ selectedProcedure.nature_terrain.join(', ') }}</p>
                  </div>
                </div>
              </div>

              <!-- Follow up checklists -->
              <div class="premium-box fr-p-3w" style="background: white">
                <h3
                  class="fr-h5"
                  style="
                    border-bottom: 1px solid var(--border-default-grey);
                    padding-bottom: 0.5rem;
                  "
                >
                  Éléments requis de procédure (Modèles réels)
                </h3>
                <div class="premium-choices-list">
                  <div
                    class="premium-action-item fr-p-1w"
                    style="cursor: pointer"
                    @click="store.toggleSuiviField(selectedProcedure.id, 'preuves')"
                  >
                    <span
                      class="fr-mr-2w"
                      :class="
                        selectedProcedure.suivi_procedure.preuves_fournies
                          ? 'fr-icon-checkbox-circle-fill'
                          : 'fr-icon-checkbox-blank-line'
                      "
                      :style="{
                        color: selectedProcedure.suivi_procedure.preuves_fournies
                          ? '#22C55E'
                          : '#9CA3AF',
                      }"
                    ></span>
                    <span class="action-label"
                      >Éléments de preuve joints au dossier (`preuves_fournies`)</span
                    >
                  </div>

                  <div
                    class="premium-action-item fr-p-1w"
                    style="cursor: pointer"
                    @click="store.toggleSuiviField(selectedProcedure.id, 'rapportSigne')"
                  >
                    <span
                      class="fr-mr-2w"
                      :class="
                        selectedProcedure.suivi_procedure.constatation_signee
                          ? 'fr-icon-checkbox-circle-fill'
                          : 'fr-icon-checkbox-blank-line'
                      "
                      :style="{
                        color: selectedProcedure.suivi_procedure.constatation_signee
                          ? '#22C55E'
                          : '#9CA3AF',
                      }"
                    ></span>
                    <span class="action-label"
                      >Rapport de constatation signé (`constatation_signee`)</span
                    >
                  </div>

                  <div
                    class="premium-action-item fr-p-1w"
                    style="cursor: pointer"
                    @click="store.toggleSuiviField(selectedProcedure.id, 'lettreSignee')"
                  >
                    <span
                      class="fr-mr-2w"
                      :class="
                        selectedProcedure.suivi_procedure.lettre_signe
                          ? 'fr-icon-checkbox-circle-fill'
                          : 'fr-icon-checkbox-blank-line'
                      "
                      :style="{
                        color: selectedProcedure.suivi_procedure.lettre_signe
                          ? '#22C55E'
                          : '#9CA3AF',
                      }"
                    ></span>
                    <span class="action-label">Lettre d'information signée (`lettre_signe`)</span>
                  </div>

                  <div
                    class="premium-action-item fr-p-1w"
                    style="cursor: pointer"
                    @click="store.toggleSuiviField(selectedProcedure.id, 'auteurIdentifie')"
                  >
                    <span
                      class="fr-icon-user-search-line fr-mr-2w"
                      style="color: var(--border-active-blue-france)"
                    ></span>
                    <span class="action-label">
                      Identification de l'auteur (`identification_reussie`) :
                      <strong>{{
                        getAuteurIdentifieText(
                          selectedProcedure.suivi_procedure.identification_reussie
                        )
                      }}</strong>
                    </span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Right Followup Panel -->
            <div class="fr-col-12 fr-col-md-5">
              <div
                class="premium-box fr-p-3w"
                style="background: white; border-left: 5px solid var(--border-active-blue-france)"
              >
                <h3
                  class="fr-h5"
                  style="
                    border-bottom: 1px solid var(--border-default-grey);
                    padding-bottom: 0.5rem;
                  "
                >
                  Pilotage déploiement
                </h3>

                <!-- Officer Assignee -->
                <div class="fr-select-group fr-mb-3w">
                  <label class="fr-label" for="assignee-select"
                    >Chargé de déploiement assigné</label
                  >
                  <select
                    id="assignee-select"
                    class="fr-select"
                    :value="selectedProcedure.suivi_procedure.charge_deploiement"
                    @change="store.assignCharge(selectedProcedure.id, $event.target.value)"
                  >
                    <option v-for="name in store.assignees" :key="name" :value="name">
                      {{ name }}
                    </option>
                  </select>
                  <p
                    v-if="selectedProcedure.suivi_procedure.date_assigned"
                    class="fr-text--xs fr-mt-1w"
                    style="color: var(--text-mention-grey)"
                  >
                    Assigné le {{ formatDate(selectedProcedure.suivi_procedure.date_assigned) }}
                  </p>
                </div>

                <!-- Internal Notes -->
                <div class="fr-input-group">
                  <label class="fr-label" for="internal-notes"
                    >Notes internes & Suivi (`observations_internes`)</label
                  >
                  <textarea
                    id="internal-notes"
                    class="fr-input"
                    placeholder="Écrivez vos notes de suivi ici (relance, appels, blocages...)"
                    style="min-height: 120px"
                    :value="selectedProcedure.suivi_procedure.observations_internes"
                    @input="store.updateNotes(selectedProcedure.id, $event.target.value)"
                  ></textarea>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- ==================================================== -->
      <!-- TAB 4: STATISTICS                                    -->
      <!-- ==================================================== -->
      <div
        v-if="currentTab === 'stats'"
        class="fr-tabs__panel fr-tabs__panel--selected"
        role="tabpanel"
      >
        <!-- OKR S2 2026 Grid -->
        <div class="fr-mb-4w">
          <h3 class="fr-h5" style="display: flex; align-items: center; gap: 0.5rem">
            <span
              class="fr-icon-notification-3-line fr-text-title-blue-france"
              aria-hidden="true"
            ></span>
            Suivi des Objectifs & Résultats Clés (OKR S2 2026)
          </h3>
          <p
            class="fr-text--sm"
            style="color: var(--text-mention-grey); margin-top: -0.5rem; margin-bottom: 1.5rem"
          >
            Cibles prioritaires de l'équipe produit d'ici au 31 décembre 2026 (les indicateurs avec
            ⚡️ sont calculés en temps réel).
          </p>
          <div class="fr-grid-row fr-grid-row--gutters">
            <div v-for="(okr, key) in liveOkrs" :key="key" class="fr-col-12 fr-col-md-4">
              <div
                class="premium-box fr-p-2w"
                style="
                  background: white;
                  border-left: 4px solid var(--border-active-blue-france);
                  height: 100%;
                  display: flex;
                  flex-direction: column;
                  justify-content: space-between;
                "
              >
                <div>
                  <div
                    class="fr-text--xs fr-mb-1v"
                    style="
                      color: var(--text-mention-grey);
                      font-weight: 700;
                      text-transform: uppercase;
                      display: flex;
                      justify-content: space-between;
                      align-items: center;
                    "
                  >
                    <span
                      >{{ key.replace('_', '.').toUpperCase() }} {{ okr.isLive ? '⚡️' : '' }}</span
                    >
                    <button
                      v-if="!okr.isLive && editingOkrKey !== key"
                      class="fr-btn fr-btn--sm fr-btn--tertiary-no-outline fr-icon-edit-line"
                      style="
                        padding: 0;
                        min-height: auto;
                        font-size: 0.8rem;
                        color: var(--border-active-blue-france);
                      "
                      title="Modifier manuellement la valeur"
                      @click="startEditOkr(key, okr.current)"
                    ></button>
                  </div>
                  <p class="fr-text--sm fr-text--bold fr-mb-2w" style="line-height: 1.3">
                    {{ okr.label }}
                  </p>
                </div>
                <div>
                  <!-- Inline OKR Editing Form -->
                  <div
                    v-if="editingOkrKey === key"
                    style="display: flex; gap: 0.5rem; align-items: center"
                    class="fr-mb-2w"
                  >
                    <input
                      type="number"
                      v-model.number="editingOkrValue"
                      class="fr-input fr-input--sm"
                      style="width: 100px"
                    />
                    <button
                      class="fr-btn fr-btn--sm fr-icon-checkbox-circle-line"
                      style="padding: 0.25rem 0.5rem"
                      title="Enregistrer"
                      @click="saveOkr(key)"
                    ></button>
                    <button
                      class="fr-btn fr-btn--sm fr-btn--secondary fr-icon-close-line"
                      style="padding: 0.25rem 0.5rem"
                      title="Annuler"
                      @click="editingOkrKey = null"
                    ></button>
                  </div>
                  <div class="fr-grid-row fr-grid-row--middle fr-mb-1v">
                    <div class="fr-col">
                      <span class="fr-text--md fr-text--bold">
                        {{ okr.current }}
                      </span>
                      <span class="fr-text--xs" style="color: var(--text-mention-grey)">
                        / {{ okr.target }} {{ okr.unit }}
                      </span>
                    </div>
                    <div class="fr-col-auto">
                      <span
                        class="bo-badge"
                        :class="
                          Math.round((okr.current / okr.target) * 100) >= 100
                            ? 'bo-badge--green'
                            : 'bo-badge--blue'
                        "
                      >
                        {{ Math.round((okr.current / okr.target) * 100) }}%
                      </span>
                    </div>
                  </div>
                  <!-- Progress Bar -->
                  <div
                    style="
                      background-color: var(--border-default-grey);
                      height: 6px;
                      border-radius: 3px;
                      width: 100%;
                      overflow: hidden;
                    "
                  >
                    <div
                      :style="{
                        width: Math.min(Math.round((okr.current / okr.target) * 100), 100) + '%',
                        backgroundColor:
                          Math.round((okr.current / okr.target) * 100) >= 100
                            ? '#22C55E'
                            : '#000091',
                        height: '100%',
                      }"
                    ></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Répartition de la charge par agent -->
        <div class="fr-mb-4w">
          <h3 class="fr-h5" style="display: flex; align-items: center; gap: 0.5rem">
            <span class="fr-icon-user-fill fr-text-title-blue-france" aria-hidden="true"></span>
            Répartition de la charge de pilotage (Dossiers réels activement suivis)
          </h3>
          <div class="fr-grid-row fr-grid-row--gutters">
            <div
              v-for="(count, agent) in store.workloadByAssignee"
              :key="agent"
              class="fr-col-12 fr-col-md-4"
            >
              <div
                class="premium-box fr-p-2w"
                style="
                  background: white;
                  border-top: 4px solid var(--border-active-blue-france);
                  text-align: center;
                "
              >
                <p class="fr-text--sm fr-mb-1v" style="color: var(--text-mention-grey)">
                  {{ agent }}
                </p>
                <p class="fr-h3 fr-mb-0">{{ count }} {{ count > 1 ? 'dossiers' : 'dossier' }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Stats Filters -->
        <div class="bo-filter-bar fr-mt-4w">
          <div class="bo-filter-group">
            <span class="bo-filter-label">Période :</span>
            <select
              v-model="statsFilters.periode"
              class="fr-select"
              style="width: auto; padding-right: 2rem"
            >
              <option value="Période globale (6 derniers mois)">
                Période globale (6 derniers mois)
              </option>
              <option value="Cette semaine">Cette semaine</option>
              <option value="Semaine dernière">Semaine dernière</option>
              <option value="Ce mois">Ce mois</option>
              <option value="Mois dernier">Mois dernier</option>
            </select>
          </div>

          <div class="bo-filter-group">
            <span class="bo-filter-label">Cas réel de dépôt sauvage:</span>
            <select
              v-model="statsFilters.exclureTests"
              class="fr-select"
              style="width: auto; padding-right: 2rem"
            >
              <option value="Oui">Oui</option>
              <option value="Non">Non</option>
            </select>
          </div>

          <div class="bo-filter-group">
            <span class="bo-filter-label">Auteur identifié :</span>
            <select
              v-model="statsFilters.auteurIdentifie"
              class="fr-select"
              style="width: auto; padding-right: 2rem"
            >
              <option value="Tous">Tous</option>
              <option value="Oui uniquement">Oui uniquement</option>
              <option value="Non uniquement">Non uniquement</option>
            </select>
          </div>
        </div>

        <!-- Render interactive stats chart -->
        <StatsChart
          :data="store.stats.history"
          title="Activité historique & Performances globales"
        />

        <!-- Compilation table of stats (matching stats-sample.md weekly tracking) -->
        <div class="fr-grid-row fr-grid-row--middle fr-mt-4w fr-mb-1w">
          <div class="fr-col">
            <h3
              class="fr-h5"
              style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0"
            >
              <span class="fr-icon-table-line fr-text-title-blue-france" aria-hidden="true"></span>
              Suivi Hebdomadaire
            </h3>
            <p class="fr-text--sm fr-mb-0" style="color: var(--text-mention-grey)">
              Données d'activité de l'équipe de déploiement, actualisées toutes les semaines.
            </p>
          </div>
          <div class="fr-col-auto">
            <button
              class="fr-btn fr-icon-add-circle-line fr-btn--icon-left"
              @click="openAddSnapshot"
            >
              Saisir une semaine
            </button>
          </div>
        </div>

        <!-- Inline snapshot entry form -->
        <div
          v-if="showSnapshotForm"
          class="premium-box fr-p-3w fr-mb-3w"
          style="background: #f6f6f6; border-left: 4px solid var(--border-active-blue-france)"
        >
          <h4 class="fr-h6 fr-mb-2w">
            {{
              editingSnapshotIndex !== -1 ? 'Modifier la semaine' : 'Saisir une nouvelle semaine'
            }}
          </h4>
          <div class="fr-grid-row fr-grid-row--gutters">
            <div class="fr-col-12 fr-col-sm-6 fr-col-md-3">
              <div class="fr-input-group">
                <label class="fr-label" for="snap-date">Date / Semaine (ex. 07/07)</label>
                <input
                  id="snap-date"
                  v-model="formSnapshot.date"
                  type="text"
                  class="fr-input"
                  placeholder="JJ/MM"
                />
              </div>
            </div>
            <div class="fr-col-12 fr-col-sm-6 fr-col-md-3">
              <div class="fr-input-group">
                <label class="fr-label" for="snap-procedures">Procédures Lancées</label>
                <input
                  id="snap-procedures"
                  v-model.number="formSnapshot.procedures"
                  type="number"
                  class="fr-input"
                />
              </div>
            </div>
            <div class="fr-col-12 fr-col-sm-6 fr-col-md-3">
              <div class="fr-input-group">
                <label class="fr-label" for="snap-col">Collectivités Actives</label>
                <input
                  id="snap-col"
                  v-model.number="formSnapshot.activeCollectivities"
                  type="number"
                  class="fr-input"
                />
              </div>
            </div>
            <div class="fr-col-12 fr-col-sm-6 fr-col-md-3">
              <div class="fr-input-group">
                <label class="fr-label" for="snap-fines">Nb Amendes Prononcées</label>
                <input
                  id="snap-fines"
                  v-model.number="formSnapshot.finesCount"
                  type="number"
                  class="fr-input"
                />
              </div>
            </div>
            <div class="fr-col-12 fr-col-sm-6 fr-col-md-3">
              <div class="fr-input-group">
                <label class="fr-label" for="snap-amount">Montant Prononcé (€)</label>
                <input
                  id="snap-amount"
                  v-model.number="formSnapshot.amountFines"
                  type="number"
                  class="fr-input"
                />
              </div>
            </div>
            <div class="fr-col-12 fr-col-sm-6 fr-col-md-3">
              <div class="fr-input-group">
                <label class="fr-label" for="snap-cleaned">Dépôts Nettoyés</label>
                <input
                  id="snap-cleaned"
                  v-model.number="formSnapshot.cleanedCount"
                  type="number"
                  class="fr-input"
                />
              </div>
            </div>
            <div class="fr-col-12 fr-col-sm-6 fr-col-md-3">
              <div class="fr-input-group">
                <label class="fr-label" for="snap-volume">Volume Nettoyé (m³)</label>
                <input
                  id="snap-volume"
                  v-model.number="formSnapshot.cleanedVolume"
                  type="number"
                  class="fr-input"
                />
              </div>
            </div>
            <div class="fr-col-12 fr-col-sm-6 fr-col-md-3">
              <div class="fr-input-group">
                <label class="fr-label" for="snap-webinars">Webinaires (Partic. cumulés)</label>
                <input
                  id="snap-webinars"
                  v-model.number="formSnapshot.webinarsCount"
                  type="number"
                  class="fr-input"
                />
              </div>
            </div>
          </div>
          <div class="fr-mt-2w" style="display: flex; gap: 1rem">
            <button class="fr-btn fr-btn--sm" @click="saveSnapshot">Enregistrer</button>
            <button class="fr-btn fr-btn--sm fr-btn--secondary" @click="showSnapshotForm = false">
              Annuler
            </button>
          </div>
        </div>

        <div class="bo-table-container">
          <table class="bo-table">
            <thead>
              <tr>
                <th>Semaine</th>
                <th>Procédures Admin Lancées (PA)</th>
                <th>Nb Collectivités Actives</th>
                <th>Nb Amendes Prononcées</th>
                <th>Montant Prononcé (€)</th>
                <th>Dépôts Nettoyés</th>
                <th>Webinaires (Participants cumulés)</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="snapshot in sortedWeeklySnapshots" :key="snapshot.date">
                <td>
                  <strong>{{ snapshot.date }}</strong>
                </td>
                <td>
                  {{ snapshot.procedures }}
                  <span
                    class="fr-text--xs"
                    style="color: var(--text-mention-grey); font-weight: 600; margin-left: 0.25rem"
                  >
                    (soit {{ Math.round((snapshot.procedures / 500) * 100) }}% de l'obj. 500)
                  </span>
                </td>
                <td>{{ snapshot.activeCollectivities }}</td>
                <td>{{ snapshot.finesCount }}</td>
                <td>
                  <strong
                    >{{
                      snapshot.amountFines.toLocaleString('fr-FR', { minimumFractionDigits: 2 })
                    }}
                    €</strong
                  >
                </td>
                <td>{{ snapshot.cleanedCount }} ({{ snapshot.cleanedVolume }}m³)</td>
                <td>{{ snapshot.webinarsCount }}</td>
                <td>
                  <div style="display: flex; gap: 0.5rem">
                    <button
                      class="fr-btn fr-btn--sm fr-btn--secondary fr-icon-edit-line"
                      style="padding: 0.25rem 0.5rem"
                      title="Modifier"
                      @click="editSnapshot(snapshot)"
                    ></button>
                    <button
                      class="fr-btn fr-btn--sm fr-btn--secondary fr-icon-delete-line"
                      style="padding: 0.25rem 0.5rem; color: #dc2626"
                      title="Supprimer"
                      @click="deleteSnapshot(snapshot.date)"
                    ></button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import StatsChart from '@/components/StatsChart.vue'
import { useBackofficeStore } from '@/stores/backoffice'
import { computed, onMounted, ref } from 'vue'

const store = useBackofficeStore()
const currentTab = ref('dashboard')
const selectedProcedureId = ref<number | null>(null)

onMounted(async () => {
  await store.fetchProcedures()
})

// Detailed filters for TAB 2
const filters = ref({
  etape: 'Tous',
  statut: 'Tous',
  charge: 'Tous',
  anomalie: 'Toutes',
  search: '',
})

// Filters for TAB 4 (Statistics)
const statsFilters = ref({
  periode: 'Période globale (6 derniers mois)',
  exclureTests: 'Oui',
  auteurIdentifie: 'Tous',
})

// Saisie manuelle des Snapshots
const showSnapshotForm = ref(false)
const editingSnapshotIndex = ref(-1)
const formSnapshot = ref({
  date: '',
  procedures: 0,
  activeCollectivities: 0,
  finesCount: 0,
  amountFines: 0,
  cleanedCount: 0,
  cleanedVolume: 0,
  webinarsCount: 0,
})

const openAddSnapshot = () => {
  editingSnapshotIndex.value = -1
  formSnapshot.value = {
    date: '',
    procedures: 0,
    activeCollectivities: 0,
    finesCount: 0,
    amountFines: 0,
    cleanedCount: 0,
    cleanedVolume: 0,
    webinarsCount: 0,
  }
  showSnapshotForm.value = true
}

const editSnapshot = (snapshot: any) => {
  editingSnapshotIndex.value = store.stats.weeklySnapshots.findIndex(
    (s) => s.date === snapshot.date
  )
  formSnapshot.value = { ...snapshot }
  showSnapshotForm.value = true
}

const saveSnapshot = () => {
  if (!formSnapshot.value.date) {
    alert('Veuillez indiquer la date / semaine.')
    return
  }
  store.saveWeeklySnapshot(formSnapshot.value)
  showSnapshotForm.value = false
}

const deleteSnapshot = (date: string) => {
  if (confirm(`Confirmer la suppression du snapshot de la semaine ${date} ?`)) {
    store.deleteWeeklySnapshot(date)
  }
}

// Inline OKR Editing states
const editingOkrKey = ref<string | null>(null)
const editingOkrValue = ref<number>(0)

const startEditOkr = (key: string, currentValue: number) => {
  editingOkrKey.value = key
  editingOkrValue.value = currentValue
}

const saveOkr = (key: string) => {
  store.updateOkrValue(key, editingOkrValue.value)
  editingOkrKey.value = null
}

const sortedWeeklySnapshots = computed(() => {
  return [...store.stats.weeklySnapshots].sort((a, b) => {
    // Basic date parsing "DD/MM" for sorting
    const [dayA, monthA] = a.date.split('/').map(Number)
    const [dayB, monthB] = b.date.split('/').map(Number)
    return monthA * 100 + dayA - (monthB * 100 + dayB)
  })
})

// Live OKR computing
const liveOkrs = computed(() => {
  const base = { ...store.stats.okrs }

  // Overwriting with live calculated values
  base.kr1_1 = {
    ...base.kr1_1,
    current: store.realProcedures.length,
    isLive: true,
  }
  base.kr1_2 = {
    ...base.kr1_2,
    current: store.liveCompletionRate,
    isLive: true,
  }
  base.kr2_2 = {
    ...base.kr2_2,
    current: store.activeCommunesCount,
    isLive: true,
  }

  return base
})

const selectedProcedure = computed(() => {
  if (!selectedProcedureId.value) return null
  return store.getProcedureById(selectedProcedureId.value)
})

const getProcedureStatut = (proc: any) => {
  const sp = proc.suivi_procedure
  if (sp.etape_en_cours === 1) {
    if (sp.identification_reussie === false) return 'Auteur non identifié'
    if (!sp.preuves_fournies || !sp.constatation_signee) return 'Pièces incomplètes'
    return 'Pièces prêtes'
  }
  if (sp.etape_en_cours === 2) {
    if (!sp.lettre_signe) return 'Lettre à signer'
    return 'Lettre à envoyer'
  }
  if (sp.etape_en_cours === 3) return 'Décision à prendre'
  if (sp.etape_en_cours === 4) return 'Exécution en cours'
  if (sp.etape_en_cours === 5) return 'Clôturé'
  return 'Inconnu'
}

const getDepuisText = (dateStr: string) => {
  if (!dateStr) return 'N/A'
  const diffTime = Math.abs(new Date().getTime() - new Date(dateStr).getTime())
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  return `${diffDays} jour${diffDays > 1 ? 's' : ''}`
}

const getAuteurIdentifieText = (val: boolean | null) => {
  if (val === true) return 'Oui'
  if (val === false) return 'Non'
  return 'Inconnu'
}

const filteredProcedures = computed(() => {
  return store.procedures.filter((proc) => {
    // Stage Filter
    if (
      filters.value.etape !== 'Tous' &&
      proc.suivi_procedure.etape_en_cours !== filters.value.etape
    )
      return false
    // Status Filter
    if (filters.value.statut !== 'Tous' && getProcedureStatut(proc) !== filters.value.statut)
      return false
    // Assignee Filter
    if (
      filters.value.charge !== 'Tous' &&
      proc.suivi_procedure.charge_deploiement !== filters.value.charge
    )
      return false
    // Anomalies Filter
    if (filters.value.anomalie === 'Avec' && !proc.suivi_procedure.anomalie) return false
    if (filters.value.anomalie === 'Sans' && proc.suivi_procedure.anomalie) return false
    // Text search (commune, agent)
    if (filters.value.search) {
      const q = filters.value.search.toLowerCase()
      const inCommune = proc.commune.toLowerCase().includes(q)
      const inAgent = proc.agent.toLowerCase().includes(q)
      if (!inCommune && !inAgent) return false
    }
    return true
  })
})

const viewDetail = (id: number) => {
  selectedProcedureId.value = id
  currentTab.value = 'detail'
}

const getBadgeClass = (status: string) => {
  if (status === 'Pièces incomplètes') return 'bo-badge bo-badge--yellow'
  if (status === 'Auteur non identifié') return 'bo-badge bo-badge--red'
  if (status === 'Décision à prendre') return 'bo-badge bo-badge--blue'
  if (status === 'Lettre à envoyer' || status === 'Lettre à signer')
    return 'bo-badge bo-badge--gray'
  return 'bo-badge bo-badge--green'
}

const getStepLabel = (step: number) => {
  const labels = ['Constatation', 'Pièces jointes', 'Notification', 'Décision', 'Exécution/Clôture']
  return labels[step - 1]
}

const formatDate = (dateStr: string | null) => {
  if (!dateStr) return 'N/A'
  const date = new Date(dateStr)
  return date.toLocaleDateString('fr-FR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
  })
}
</script>

<style scoped>
@import '@/styles/backoffice.css';

.style-icon {
  font-size: 1.15rem;
}
</style>
