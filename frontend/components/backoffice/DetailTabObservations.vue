<template>
  <div
    v-if="procedure.suivi_procedure?.observations_internes"
    class="premium-box fr-p-3w fr-mb-3w bo-card bo-card--obs"
  >
    <h3 class="fr-h6 fr-mb-2w bo-card-title">
      <span class="fr-icon-clipboard-line fr-mr-1w"></span> Observations Internes
    </h3>
    <p class="bo-obs-text fr-mb-2w">
      {{ procedure.suivi_procedure.observations_internes }}
    </p>
    <p
      v-if="procedure.suivi_procedure.date_pilotage"
      class="fr-text--xs fr-mb-0 fr-text-mention--grey bo-obs-date"
    >
      Date de pilotage : <strong>{{ formatDate(procedure.suivi_procedure.date_pilotage) }}</strong>
    </p>
  </div>
</template>

<script setup lang="ts">
import { formatDate } from '@/utils/date'

defineProps<{
  procedure: any
}>()
</script>
