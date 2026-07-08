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
            <option :value="0">0 Constatation</option>
            <option :value="1">1 Pièces jointes</option>
            <option :value="2">2 Notification</option>
            <option :value="3">3 Décision</option>
            <option :value="4">4 Sanctionner</option>
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
          <label class="bo-filter-label" for="filter-assignee">Assigné à</label>
          <select id="filter-assignee" v-model="filters.assignee" class="fr-select">
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

    <!-- Count display / info bar -->
    <div class="fr-mb-2w bo-info-bar">
      <span class="fr-text--sm fr-text-mention--grey">
        Nombre de procédures : <strong>{{ filteredProcedures.length }}</strong>
        <span v-if="filteredProcedures.length !== store.procedures.length">
          sur {{ store.procedures.length }} au total
        </span>
      </span>
    </div>

    <!-- Procedures Grid Table -->
    <div class="bo-table-container">
      <table class="bo-table">
        <thead>
          <tr>
            <th class="bo-th-customizer">
              <!-- Column Customizer -->
              <div class="bo-customizer-container">
                <button
                  class="fr-btn fr-btn--sm fr-btn--tertiary-no-outline bo-customizer-btn-toggle"
                  @click="showCustomizer = !showCustomizer"
                  title="Personnaliser les colonnes"
                >
                  <span class="fr-icon-settings-5-line" aria-hidden="true"></span>
                </button>
                <div
                  v-if="showCustomizer"
                  class="bo-customizer-popover bo-customizer-popover--left"
                >
                  <div class="bo-customizer-header">
                    <div class="bo-customizer-title bo-customizer-title--no-border">
                      Colonnes à afficher
                    </div>
                    <button
                      class="fr-btn fr-btn--sm fr-btn--tertiary-no-outline bo-btn-close-sm"
                      @click="showCustomizer = false"
                      aria-label="Fermer"
                    >
                      <span class="fr-icon-close-line" aria-hidden="true"></span>
                    </button>
                  </div>
                  <div class="bo-customizer-list">
                    <label
                      v-for="col in customizableColumns"
                      :key="col.key"
                      class="bo-customizer-item"
                    >
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
                  {{
                    getStepLabel(
                      procedure.suivi_procedure.etape_en_cours,
                      procedure.auteur_identifie
                    )
                  }}
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
                      <DetailTabObservations :procedure="procedure" />
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
  parseQueryParam,
} from '@/utils/backoffice'
import { formatConstatationDate } from '@/utils/date'
import { computed, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import DetailTabAuthor from '@/components/backoffice/DetailTabAuthor.vue'
import DetailTabDescription from '@/components/backoffice/DetailTabDescription.vue'
import DetailTabDocuments from '@/components/backoffice/DetailTabDocuments.vue'
import DetailTabGeneral from '@/components/backoffice/DetailTabGeneral.vue'
import DetailTabObservations from '@/components/backoffice/DetailTabObservations.vue'
import DetailTabPrejudice from '@/components/backoffice/DetailTabPrejudice.vue'

const store = useBackofficeStore()
const route = useRoute()
const router = useRouter()

defineEmits<{
  (e: 'view-detail', id: number): void
}>()

const filters = ref({
  etape: parseQueryParam(route.query.etape, 'Tous'),
  traitement: parseQueryParam(route.query.traitement, 'Tous'),
  assignee: parseQueryParam(route.query.assignee, 'Tous'),
  casReels: parseQueryParam(route.query.casReels, 'Oui'),
  auteurIdentifie: parseQueryParam(route.query.auteurIdentifie, 'Tous'),
  search: parseQueryParam(route.query.search, ''),
})

// Sync filters changes with route queries
watch(
  filters,
  (newFilters) => {
    const query = { ...route.query }

    if (newFilters.etape && newFilters.etape !== 'Tous') {
      query.etape = newFilters.etape.toString()
    } else {
      delete query.etape
    }

    if (newFilters.traitement && newFilters.traitement !== 'Tous') {
      query.traitement = newFilters.traitement
    } else {
      delete query.traitement
    }

    if (newFilters.assignee && newFilters.assignee !== 'Tous') {
      query.assignee = newFilters.assignee
    } else {
      delete query.assignee
    }

    if (newFilters.casReels && newFilters.casReels !== 'Oui') {
      query.casReels = newFilters.casReels
    } else {
      delete query.casReels
    }

    if (newFilters.auteurIdentifie && newFilters.auteurIdentifie !== 'Tous') {
      query.auteurIdentifie = newFilters.auteurIdentifie
    } else {
      delete query.auteurIdentifie
    }

    if (newFilters.search) {
      query.search = newFilters.search
    } else {
      delete query.search
    }

    router.replace({ query })
  },
  { deep: true }
)

// Sync route query changes back to local filters (e.g. browser back/forward)
watch(
  () => route.query,
  (newQuery) => {
    if (route.path === '/procedures-liste') {
      filters.value.etape = parseQueryParam(newQuery.etape, 'Tous')
      filters.value.traitement = parseQueryParam(newQuery.traitement, 'Tous')
      filters.value.assignee = parseQueryParam(newQuery.assignee, 'Tous')
      filters.value.casReels = parseQueryParam(newQuery.casReels, 'Oui')
      filters.value.auteurIdentifie = parseQueryParam(newQuery.auteurIdentifie, 'Tous')
      filters.value.search = parseQueryParam(newQuery.search, '')
    }
  }
)

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
    if (filters.value.assignee !== 'Tous') {
      const assigned = procedure.suivi_procedure.personne_assignee
      if (filters.value.assignee === 'None') {
        if (assigned !== null) return false
      } else if (assigned !== Number(filters.value.assignee)) {
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
