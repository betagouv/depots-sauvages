<template>
  <div class="fr-tabs__panel fr-tabs__panel--selected" role="tabpanel">
    <div v-if="!selectedProcedure" class="fr-text-center fr-py-5w">
      <span class="fr-icon-arrow-left-line fr-mr-1w" aria-hidden="true"></span>
      Veuillez sélectionner une procédure dans le tableau de bord ou la liste pour afficher ses
      détails.
    </div>

    <div v-else>
      <!-- Stepper/Timeline progress bar -->
      <StepperTimeline
        :current-step="selectedProcedure.suivi_procedure.etape_en_cours"
        :auteur-identifie="selectedProcedure.auteur_identifie"
      />

      <div class="fr-grid-row fr-grid-row--gutters">
        <!-- Left Column: Constatation Details -->
        <div class="fr-col-12 fr-col-md-7">
          <DetailTabGeneral :procedure="selectedProcedure" />
          <DetailTabDescription :procedure="selectedProcedure" />
          <DetailTabAuthor :procedure="selectedProcedure" />
          <DetailTabPrejudice :procedure="selectedProcedure" />
          <DetailTabDocuments :procedure="selectedProcedure" />
        </div>

        <!-- Right Column: Suivi de Procédure Checklist & Pilotage -->
        <div class="fr-col-12 fr-col-md-5">
          <DetailTabPilotage :procedure="selectedProcedure" />
          <DetailTabObservations :procedure="selectedProcedure" />
          <DetailTabSuiviActions :procedure="selectedProcedure" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useBackofficeStore } from '@/stores/backoffice'
import { computed } from 'vue'

import StepperTimeline from '@/components/StepperTimeline.vue'
import DetailTabAuthor from '@/components/backoffice/DetailTabAuthor.vue'
import DetailTabDescription from '@/components/backoffice/DetailTabDescription.vue'
import DetailTabDocuments from '@/components/backoffice/DetailTabDocuments.vue'
import DetailTabGeneral from '@/components/backoffice/DetailTabGeneral.vue'
import DetailTabObservations from '@/components/backoffice/DetailTabObservations.vue'
import DetailTabPilotage from '@/components/backoffice/DetailTabPilotage.vue'
import DetailTabPrejudice from '@/components/backoffice/DetailTabPrejudice.vue'
import DetailTabSuiviActions from '@/components/backoffice/DetailTabSuiviActions.vue'

const store = useBackofficeStore()

const props = defineProps<{
  selectedProcedureId: number | null
}>()

const selectedProcedure = computed(() => {
  if (!props.selectedProcedureId) return null
  return store.getProcedureById(props.selectedProcedureId)
})
</script>

<style scoped>
.premium-box {
  background-color: #ffffff;
  border: 1px solid var(--border-default-grey);
}
</style>
