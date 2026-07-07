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
            <th>ID</th>
            <th>Commune</th>
            <th>Agent constatant</th>
            <th>Date Constat</th>
            <th>Étape</th>
            <th>Traitement</th>
            <th>Montant amende</th>
            <th>Assigné à</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="procedure in filteredProcedures" :key="procedure.id">
            <td>
              <code>#{{ procedure.id }}</code>
            </td>
            <td>
              <strong>{{ procedure.commune }}</strong>
            </td>
            <td>{{ procedure.agent }}</td>
            <td>{{ formatConstatationDate(procedure.date_constat) }}</td>
            <td>
              <span :class="getBadgeClass(procedure.suivi_procedure.etape_en_cours)">
                {{ procedure.suivi_procedure.etape_en_cours }}.
                {{ getStepLabel(procedure.suivi_procedure.etape_en_cours) }}
              </span>
            </td>
            <td>
              <span :class="getTraitementBadgeClass(getProcedureTraitement(procedure))">
                {{ getProcedureTraitement(procedure) }}
              </span>
            </td>
            <td>
              <span v-if="procedure.suivi_procedure.montant_amende">
                {{ procedure.suivi_procedure.montant_amende }} €
              </span>
              <span v-else class="fr-text-mention--grey">-</span>
            </td>
            <td>
              {{
                store.assignees.find((a) => a.id === procedure.suivi_procedure.personne_assignee)?.name ||
                'Non assigné'
              }}
            </td>
            <td>
              <button
                class="fr-btn fr-btn--sm fr-btn--secondary"
                @click="$emit('view-detail', procedure.id)"
              >
                Consulter
              </button>
            </td>
          </tr>
          <tr v-if="filteredProcedures.length === 0">
            <td colspan="9" class="fr-text-center fr-py-3w fr-text-mention--grey">
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
