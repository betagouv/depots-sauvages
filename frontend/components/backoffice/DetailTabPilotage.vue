<template>
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
        :value="procedure.suivi_procedure?.charge_deploiement"
        @change="
          store.assignCharge(
            procedure.id,
            ($event.target as HTMLSelectElement).value
          )
        "
      >
        <option v-for="name in store.assignees" :key="name" :value="name">
          {{ name }}
        </option>
      </select>
      <p
        v-if="procedure.suivi_procedure?.date_assigned"
        class="fr-text--xs fr-mt-1w fr-mb-0"
        style="color: var(--text-mention-grey)"
      >
        Assigné le {{ formatDate(procedure.suivi_procedure.date_assigned) }}
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
        :value="procedure.suivi_procedure?.observations_internes"
        @change="
          store.updateNotes(
            procedure.id,
            ($event.target as HTMLTextAreaElement).value
          )
        "
      ></textarea>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useBackofficeStore } from '@/stores/backoffice'
import { formatDate } from '@/utils/backoffice'

const store = useBackofficeStore()

defineProps<{
  procedure: any
}>()
</script>
