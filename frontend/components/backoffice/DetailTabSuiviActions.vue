<template>
  <div class="premium-box fr-p-3w bo-card">
    <h3 class="fr-h6 fr-mb-3w bo-card-title">
      <span class="fr-icon-survey-line fr-mr-1w"></span> Actions du Suivi
    </h3>

    <DetailTabSuiviActionsAuteurIdentifie v-if="auteurIdentifie" :procedure="procedure" />
    <DetailTabSuiviActionsAuteurNonIdentifie v-else :procedure="procedure" />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import DetailTabSuiviActionsAuteurIdentifie from './DetailTabSuiviActionsAuteurIdentifie.vue'
import DetailTabSuiviActionsAuteurNonIdentifie from './DetailTabSuiviActionsAuteurNonIdentifie.vue'

const props = defineProps<{
  procedure: any
}>()

const auteurIdentifie = computed(() => props.procedure?.auteur_identifie ?? false)
</script>
