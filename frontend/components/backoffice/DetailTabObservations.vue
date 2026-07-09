<template>
  <div
    v-if="procedure.suivi_procedure?.observations_internes"
    class="premium-box fr-p-3w fr-mb-3w bo-card"
  >
    <h3 class="fr-h6 fr-mb-2w bo-card-title">
      <span class="fr-icon-clipboard-line fr-mr-1w"></span> Observations de la collectivité
    </h3>
    <p class="bo-obs-text fr-mb-0">
      {{ procedure.suivi_procedure.observations_internes }}
    </p>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  procedure: any
}>()
</script>
