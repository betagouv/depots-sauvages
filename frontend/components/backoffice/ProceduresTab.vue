<template>
  <div class="fr-tabs__panel fr-tabs__panel--selected" role="tabpanel">
    <!-- Filter Bar -->
    <div class="bo-filter-bar">
      <div class="bo-filter-group">
        <span class="bo-filter-label">Étape :</span>
        <select v-model="filters.etape" class="fr-select" style="width: auto; padding-right: 2rem">
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
        <select v-model="filters.statut" class="fr-select" style="width: auto; padding-right: 2rem">
          <option value="Tous">Tous</option>
          <option value="Pièces incomplètes">Pièces incomplètes</option>
          <option value="Auteur non identifié">Auteur non identifié</option>
          <option value="Décision à prendre">Décision à prendre</option>
          <option value="Lettre à envoyer">Lettre à envoyer</option>
        </select>
      </div>

      <div class="bo-filter-group">
        <span class="bo-filter-label">Chargé :</span>
        <select v-model="filters.charge" class="fr-select" style="width: auto; padding-right: 2rem">
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
              <span :class="getBadgeClass(getProcedureStatut(procedure))">
                ● Étape {{ procedure.suivi_procedure.etape_en_cours }} :
                {{ getProcedureStatut(procedure) }}
              </span>
            </td>
            <td>
              {{
                store.assignees.find((a) => a.id === procedure.suivi_procedure.assigned_to)?.name ||
                'Non assigné'
              }}
            </td>
            <td>
              <span
                v-if="procedure.suivi_procedure.anomalie"
                class="fr-text--xs"
                style="color: #dc2626; font-weight: 700"
              >
                ⚠ {{ procedure.suivi_procedure.anomalie }}
              </span>
              <span v-else class="fr-text--xs" style="color: #9ca3af">Aucune</span>
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
            <td colspan="8" class="fr-text-center fr-py-3w" style="color: var(--text-mention-grey)">
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
import { getBadgeClass, getProcedureStatut } from '@/utils/backoffice'
import { formatConstatationDate } from '@/utils/date'
import { computed, ref } from 'vue'

const store = useBackofficeStore()

defineEmits<{
  (e: 'view-detail', id: number): void
}>()

const filters = ref({
  etape: 'Tous',
  statut: 'Tous',
  charge: 'Tous',
  anomalie: 'Toutes',
  search: '',
})

const filteredProcedures = computed(() => {
  return store.procedures.filter((procedure) => {
    if (
      filters.value.etape !== 'Tous' &&
      procedure.suivi_procedure.etape_en_cours !== filters.value.etape
    )
      return false
    if (filters.value.statut !== 'Tous' && getProcedureStatut(procedure) !== filters.value.statut)
      return false
    if (filters.value.charge !== 'Tous') {
      const assigned = procedure.suivi_procedure.assigned_to
      if (filters.value.charge === 'None') {
        if (assigned !== null) return false
      } else if (assigned !== Number(filters.value.charge)) {
        return false
      }
    }
    if (filters.value.anomalie === 'Avec' && !procedure.suivi_procedure.anomalie) return false
    if (filters.value.anomalie === 'Sans' && procedure.suivi_procedure.anomalie) return false
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
