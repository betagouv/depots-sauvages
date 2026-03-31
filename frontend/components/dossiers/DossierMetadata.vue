<template>
  <div class="dossier-metadata">
    <div v-if="dossier.date_creation" class="fr-text--xs fr-text-mention--grey fr-mb-2w">
      <span class="fr-icon-calendar-line fr-icon--sm fr-mr-1v" aria-hidden="true"></span>
      Créé le {{ formatDate(dossier.date_creation) }}
      <span v-if="shouldShowModificationDate(dossier.date_creation, dossier.date_modification)">
        &middot; Modifié le {{ formatDate(dossier.date_modification) }}
      </span>
    </div>
    <div v-if="dossier.date_constat || dossier.localisation_depot">
      <div class="fr-grid-row fr-grid-row--gutters">
        <div v-if="dossier.date_constat" class="fr-col-12 fr-col-md-6 fr-text--sm">
          <div class="fr-display-flex fr-align-items-center fr-mb-1v">
            <span
              class="fr-icon-calendar-line fr-icon--sm fr-mr-1v fr-text-active--blue-france"
              aria-hidden="true"
            ></span>
            <strong>Date de constatation :</strong>
          </div>
          <div class="fr-ml-3w fr-text-title--grey">
            {{ formatDate(dossier.date_constat) }}
          </div>
        </div>
        <div v-if="dossier.localisation_depot" class="fr-col-12 fr-col-md-6 fr-text--sm">
          <div class="fr-display-flex fr-align-items-center fr-mb-1v">
            <span
              class="fr-icon-map-pin-2-line fr-icon--sm fr-mr-1v fr-text-active--blue-france"
              aria-hidden="true"
            ></span>
            <strong>Adresse du dépôt :</strong>
          </div>
          <div class="fr-ml-3w fr-text-title--grey">
            {{ dossier.localisation_depot }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { formatDate, shouldShowModificationDate } from '../../utils/date'

interface DossierData {
  date_creation?: string
  date_modification?: string | null
  date_constat?: string | null
  localisation_depot?: string | null
}

defineProps<{
  dossier: DossierData
}>()
</script>

<style scoped>
.dossier-metadata {
  width: 100%;
}
</style>
