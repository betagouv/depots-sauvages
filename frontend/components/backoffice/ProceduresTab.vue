<template>
  <div class="fr-tabs__panel fr-tabs__panel--selected" role="tabpanel">
    <!-- Filter Bar -->
    <div class="bo-filter-bar-container">
      <div class="bo-search-row">
        <label class="bo-filter-label" for="search-input">Rechercher</label>
        <input
          id="search-input"
          v-model="filters.search"
          type="text"
          class="fr-input bo-w-full"
          placeholder="🔍 Rechercher une commune ou agent..."
        />
      </div>

      <div class="bo-filters-grid">
        <div class="bo-filter-group-vertical">
          <label class="bo-filter-label" for="filter-etape">Étape</label>
          <select id="filter-etape" v-model="filters.etape" class="fr-select">
            <option value="Tous">Tous</option>
            <option :value="1">1 Constatation</option>
            <option :value="2">2 Pièces jointes</option>
            <option :value="3">3 Notification</option>
            <option :value="4">4 Décision</option>
            <option :value="5">5 Clôture</option>
          </select>
        </div>

        <div class="bo-filter-group-vertical">
          <label class="bo-filter-label" for="filter-traitement">Statut traitement</label>
          <select id="filter-traitement" v-model="filters.traitement" class="fr-select">
            <option value="Tous">Tous</option>
            <option value="Nouveau">Nouveau</option>
            <option value="Ouvert">Ouvert</option>
            <option value="En pause">En pause</option>
            <option value="Résolu">Résolu</option>
            <option value="Clôturé">Clôturé</option>
          </select>
        </div>

        <div class="bo-filter-group-vertical">
          <label class="bo-filter-label" for="filter-charge">Assigné à</label>
          <select id="filter-charge" v-model="filters.charge" class="fr-select">
            <option value="Tous">Tous</option>
            <option
              v-for="assignee in store.assignees"
              :key="assignee.id ?? 'unassigned'"
              :value="assignee.id ?? 'None'"
            >
              {{ assignee.name }}
            </option>
          </select>
        </div>

        <div class="bo-filter-group-vertical">
          <label class="bo-filter-label" for="filter-cas-reels">Cas réels</label>
          <select id="filter-cas-reels" v-model="filters.casReels" class="fr-select">
            <option value="Tous">Tous</option>
            <option value="Oui">Oui</option>
            <option value="Non">Non</option>
          </select>
        </div>

        <div class="bo-filter-group-vertical">
          <label class="bo-filter-label" for="filter-auteur-identifie">Auteur identifié</label>
          <select id="filter-auteur-identifie" v-model="filters.auteurIdentifie" class="fr-select">
            <option value="Tous">Tous</option>
            <option value="Oui">Oui</option>
            <option value="Non">Non</option>
          </select>
        </div>
      </div>
    </div>

    <!-- Procedures Grid Table -->
    <div class="bo-table-container">
      <table class="bo-table">
        <thead>
          <tr>
            <th style="width: 40px; position: relative; text-align: center; vertical-align: middle; padding: 0.25rem;">
              <!-- Column Customizer -->
              <div class="bo-customizer-container">
                <button
                  class="fr-btn fr-btn--sm fr-btn--tertiary-no-outline"
                  style="padding: 0.25rem; min-height: auto; width: 28px; height: 28px; display: inline-flex; align-items: center; justify-content: center;"
                  @click="showCustomizer = !showCustomizer"
                  title="Personnaliser les colonnes"
                >
                  <span class="fr-icon-settings-5-line" aria-hidden="true" style="margin: 0;"></span>
                </button>
                <div v-if="showCustomizer" class="bo-customizer-popover" style="left: 0; right: auto; text-align: left;">
                  <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border-default-grey); padding-bottom: 0.5rem; margin-bottom: 0.75rem;">
                    <div class="bo-customizer-title" style="margin-bottom: 0; border-bottom: none; padding-bottom: 0;">Colonnes à afficher</div>
                    <button
                      class="fr-btn fr-btn--sm fr-btn--tertiary-no-outline"
                      style="padding: 0.25rem; min-height: auto;"
                      @click="showCustomizer = false"
                      aria-label="Fermer"
                    >
                      <span class="fr-icon-close-line" aria-hidden="true"></span>
                    </button>
                  </div>
                  <div class="bo-customizer-list">
                    <label v-for="col in customizableColumns" :key="col.key" class="bo-customizer-item">
                      <input type="checkbox" v-model="visibleColumns[col.key]" />
                      <span>{{ col.label }}</span>
                    </label>
                  </div>
                </div>
              </div>
            </th>
            <th v-if="visibleColumns.id">ID</th>
            <th v-if="visibleColumns.commune">Commune</th>
            <th v-if="visibleColumns.agent">Agent constatant</th>
            <th v-if="visibleColumns.date_constat">Date Constat</th>
            <th v-if="visibleColumns.etape">Étape</th>
            <th v-if="visibleColumns.traitement">Traitement</th>
            <th v-if="visibleColumns.montant_amende">Montant amende</th>
            <th v-if="visibleColumns.montant_prejudice">Montant préjudice</th>
            <th v-if="visibleColumns.assigne_a">Assigné à</th>
            <th v-if="visibleColumns.actions">Actions</th>
          </tr>
        </thead>
        <tbody>
          <template v-for="procedure in filteredProcedures" :key="procedure.id">
            <tr>
              <td>
                <button
                  class="bo-chevron-btn"
                  :class="{ 'bo-chevron-btn--expanded': isExpanded(procedure.id) }"
                  @click="toggleRow(procedure.id)"
                  :aria-label="
                    isExpanded(procedure.id) ? 'Masquer les détails' : 'Afficher les détails'
                  "
                >
                  <span class="fr-icon-arrow-right-s-line" aria-hidden="true"></span>
                </button>
              </td>
              <td v-if="visibleColumns.id">
                <code>#{{ procedure.id }}</code>
              </td>
              <td v-if="visibleColumns.commune">
                <strong>{{ procedure.commune }}</strong>
              </td>
              <td v-if="visibleColumns.agent">{{ procedure.agent }}</td>
              <td v-if="visibleColumns.date_constat">
                {{ formatConstatationDate(procedure.date_constat) }}
              </td>
              <td v-if="visibleColumns.etape">
                <span :class="getBadgeClass(procedure.suivi_procedure.etape_en_cours)">
                  {{ procedure.suivi_procedure.etape_en_cours }}.
                  {{ getStepLabel(procedure.suivi_procedure.etape_en_cours, procedure.auteur_identifie) }}
                </span>
              </td>
              <td v-if="visibleColumns.traitement">
                <span :class="getTraitementBadgeClass(getProcedureTraitement(procedure))">
                  {{ getProcedureTraitement(procedure) }}
                </span>
              </td>
              <td v-if="visibleColumns.montant_amende">
                <span v-if="procedure.suivi_procedure.montant_amende">
                  {{ procedure.suivi_procedure.montant_amende }} €
                </span>
                <span v-else class="fr-text-mention--grey">-</span>
              </td>
              <td v-if="visibleColumns.montant_prejudice">
                <span v-if="procedure.prejudice_montant">
                  {{ procedure.prejudice_montant }} €
                </span>
                <span v-else class="fr-text-mention--grey">-</span>
              </td>
              <td v-if="visibleColumns.assigne_a">
                {{
                  store.assignees.find((a) => a.id === procedure.suivi_procedure.personne_assignee)
                    ?.name || 'Non assigné'
                }}
              </td>
              <td v-if="visibleColumns.actions">
                <button
                  class="fr-btn fr-btn--sm fr-btn--secondary"
                  @click="$emit('view-detail', procedure.id)"
                >
                  Consulter
                </button>
              </td>
            </tr>
            <tr v-if="isExpanded(procedure.id)" class="bo-accordion-tr">
              <td :colspan="activeColumnsCount" class="bo-accordion-td">
                <div class="bo-accordion-content">
                  <div class="fr-grid-row fr-grid-row--gutters">
                    <div class="fr-col-12 fr-col-md-6 fr-col-lg-4">
                      <DetailTabGeneral :procedure="procedure" />
                    </div>
                    <div class="fr-col-12 fr-col-md-6 fr-col-lg-4">
                      <DetailTabDescription :procedure="procedure" />
                    </div>
                    <div class="fr-col-12 fr-col-md-6 fr-col-lg-4">
                      <DetailTabAuthor :procedure="procedure" />
                    </div>
                    <div class="fr-col-12 fr-col-md-6 fr-col-lg-4">
                      <DetailTabPrejudice :procedure="procedure" />
                    </div>
                    <div class="fr-col-12 fr-col-md-6 fr-col-lg-4">
                      <DetailTabDocuments :procedure="procedure" />
                    </div>
                    <div
                      class="fr-col-12 fr-col-md-6 fr-col-lg-4"
                      v-if="procedure.suivi_procedure.observations_internes"
                    >
                      <div
                        class="premium-box fr-p-3w fr-mb-3w bo-card"
                        style="height: 100%; min-height: 200px"
                      >
                        <h3 class="fr-h6 fr-mb-2w bo-card-title">
                          <span class="fr-icon-clipboard-line fr-mr-1w"></span> Observations
                          Internes
                        </h3>
                        <p class="bo-obs-text fr-mb-0">
                          {{ procedure.suivi_procedure.observations_internes }}
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              </td>
            </tr>
          </template>
          <tr v-if="filteredProcedures.length === 0">
            <td :colspan="activeColumnsCount" class="fr-text-center fr-py-3w fr-text-mention--grey">
              Aucune procédure ne correspond aux filtres appliqués.
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useBackofficeStore } from '@/stores/backoffice'
import {
  getBadgeClass,
  getProcedureTraitement,
  getStepLabel,
  getTraitementBadgeClass,
} from '@/utils/backoffice'
import { formatConstatationDate } from '@/utils/date'
import { computed, ref } from 'vue'

import DetailTabAuthor from '@/components/backoffice/DetailTabAuthor.vue'
import DetailTabDescription from '@/components/backoffice/DetailTabDescription.vue'
import DetailTabDocuments from '@/components/backoffice/DetailTabDocuments.vue'
import DetailTabGeneral from '@/components/backoffice/DetailTabGeneral.vue'
import DetailTabPrejudice from '@/components/backoffice/DetailTabPrejudice.vue'

const store = useBackofficeStore()

defineEmits<{
  (e: 'view-detail', id: number): void
}>()

const filters = ref({
  etape: 'Tous',
  traitement: 'Tous',
  charge: 'Tous',
  casReels: 'Oui',
  auteurIdentifie: 'Tous',
  search: '',
})

// Column customization state
const showCustomizer = ref(false)
const visibleColumns = ref<Record<string, boolean>>({
  id: true,
  commune: true,
  agent: true,
  date_constat: true,
  etape: true,
  traitement: true,
  montant_amende: false,
  montant_prejudice: false,
  assigne_a: true,
  actions: true,
})

const customizableColumns = [
  { key: 'agent', label: 'Agent constatant' },
  { key: 'date_constat', label: 'Date Constat' },
  { key: 'etape', label: 'Étape active' },
  { key: 'traitement', label: 'Statut traitement' },
  { key: 'montant_amende', label: 'Montant amende' },
  { key: 'montant_prejudice', label: 'Montant préjudice' },
  { key: 'assigne_a', label: 'Assigné à' },
]

// Accordion (expanded rows) state
const expandedRows = ref<Set<number>>(new Set())

const toggleRow = (id: number) => {
  if (expandedRows.value.has(id)) {
    expandedRows.value.delete(id)
  } else {
    expandedRows.value.add(id)
  }
}

const isExpanded = (id: number) => expandedRows.value.has(id)

// Active column count for colspan
const activeColumnsCount = computed(() => {
  return Object.values(visibleColumns.value).filter(Boolean).length + 1 // +1 for the chevron column
})

const filteredProcedures = computed(() => {
  return store.procedures.filter((procedure) => {
    if (
      filters.value.etape !== 'Tous' &&
      procedure.suivi_procedure.etape_en_cours !== filters.value.etape
    )
      return false
    if (
      filters.value.traitement !== 'Tous' &&
      getProcedureTraitement(procedure) !== filters.value.traitement
    )
      return false
    if (filters.value.charge !== 'Tous') {
      const assigned = procedure.suivi_procedure.personne_assignee
      if (filters.value.charge === 'None') {
        if (assigned !== null) return false
      } else if (assigned !== Number(filters.value.charge)) {
        return false
      }
    }
    if (filters.value.casReels === 'Oui' && procedure.ceci_est_un_test) return false
    if (filters.value.casReels === 'Non' && !procedure.ceci_est_un_test) return false
    if (filters.value.auteurIdentifie === 'Oui' && !procedure.auteur_identifie) return false
    if (filters.value.auteurIdentifie === 'Non' && procedure.auteur_identifie) return false
    if (filters.value.search) {
      const q = filters.value.search.toLowerCase()
      const inCommune = procedure.commune.toLowerCase().includes(q)
      const inAgent = procedure.agent.toLowerCase().includes(q)
      if (!inCommune && !inAgent) return false
    }
    return true
  })
})
</script>
