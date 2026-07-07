<template>
  <div class="premium-box fr-p-3w fr-mb-3w bo-card bo-card--accent-blue">
    <h3 class="fr-h6 fr-mb-2w fr-text-title--blue-france">
      <span class="fr-icon-user-setting-line fr-mr-1w"></span> Pilotage dossier
    </h3>
    <div class="fr-select-group fr-mb-2w">
      <label class="fr-label fr-text--xs" for="assignee-select">Assigné à</label>
      <select
        id="assignee-select"
        class="fr-select"
        :value="procedure.suivi_procedure?.assigned_to ?? ''"
        @change="
          store.assignCharge(
            procedure.id,
            ($event.target as HTMLSelectElement).value
              ? Number(($event.target as HTMLSelectElement).value)
              : null
          )
        "
      >
        <option
          v-for="assignee in store.assignees"
          :key="assignee.id ?? 'unassigned'"
          :value="assignee.id ?? ''"
        >
          {{ assignee.name }}
        </option>
      </select>
      <p
        v-if="procedure.suivi_procedure?.assigned_at"
        class="fr-text--xs fr-mt-1w fr-mb-0 fr-text-mention--grey"
      >
        Assignation mise à jour le {{ formatDate(procedure.suivi_procedure.assigned_at) }}
      </p>
    </div>

    <!-- Internal Notes -->
    <div class="fr-input-group fr-mb-0">
      <label class="fr-label fr-text--xs" for="internal-notes">Notes de suivi & Observations</label>
      <textarea
        id="internal-notes"
        class="fr-input bo-textarea-obs"
        placeholder="Relance, appels, blocages..."
        :value="procedure.suivi_procedure?.observations_internes"
        @change="store.updateNotes(procedure.id, ($event.target as HTMLTextAreaElement).value)"
      ></textarea>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useBackofficeStore } from '@/stores/backoffice'
import { formatDate } from '@/utils/date'

const store = useBackofficeStore()

defineProps<{
  procedure: any
}>()
</script>
