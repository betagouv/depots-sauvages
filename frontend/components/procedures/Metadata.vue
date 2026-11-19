<template>
  <div class="procedure-metadata">
    <div v-if="procedure.date_creation || suivi?.modified" class="fr-text--xs fr-text-mention--grey fr-mb-2w metadata-timestamps">
      <div v-if="procedure.date_creation" class="fr-mb-1v">
        <span class="fr-icon-calendar-line fr-icon--sm fr-mr-1v" aria-hidden="true"></span>
        Constat initial créé le {{ formatDate(procedure.date_creation) }}<template v-if="procedure.created_by_name"> par <strong>{{ procedure.created_by_name }}</strong></template>
        <span v-if="shouldShowModificationDate(procedure.date_creation, procedure.date_modification)">
          &middot; Constatation modifiée le {{ formatDate(procedure.date_modification) }}<template v-if="procedure.updated_by_name"> par <strong>{{ procedure.updated_by_name }}</strong></template>
        </span>
      </div>
      <div v-if="shouldShowSuiviModification(procedure.date_creation, suivi?.modified)" class="fr-text--xs">
        <span class="fr-icon-refresh-line fr-icon--sm fr-mr-1v" aria-hidden="true"></span>
        Dernière action de suivi le {{ formatDate(suivi?.modified) }}<template v-if="suivi?.updated_by_name"> par <strong>{{ suivi.updated_by_name }}</strong></template>
      </div>
    </div>
    <div v-if="procedure.date_constat || procedure.localisation_depot">
      <div class="fr-grid-row fr-grid-row--gutters">
        <div v-if="procedure.date_constat" class="fr-col-12 fr-col-md-6 fr-text--sm">
          <div class="fr-display-flex fr-align-items-center fr-mb-1v">
            <span
              class="fr-icon-calendar-line fr-icon--sm fr-mr-1v fr-text-active--blue-france"
              aria-hidden="true"
            ></span>
            <strong>Date de constatation :</strong>
          </div>
          <div class="fr-ml-3w fr-text-title--grey">
            {{ formatConstatationDate(procedure.date_constat, procedure.heure_constat) }}
          </div>
        </div>
        <div v-if="procedure.localisation_depot" class="fr-col-12 fr-col-md-6 fr-text--sm">
          <div class="fr-display-flex fr-align-items-center fr-mb-1v">
            <span
              class="fr-icon-map-pin-2-line fr-icon--sm fr-mr-1v fr-text-active--blue-france"
              aria-hidden="true"
            ></span>
            <strong>Adresse du dépôt :</strong>
          </div>
          <div class="fr-ml-3w fr-text-title--grey">
            {{ procedure.localisation_depot }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { SuiviProcedure } from '../../stores/suivi-procedure'
import { formatConstatationDate, formatDate, shouldShowModificationDate } from '../../utils/date'

interface ProcedureData {
  date_creation?: string
  date_modification?: string | null
  created_by_name?: string | null
  updated_by_name?: string | null
  date_constat?: string | null
  heure_constat?: string | null
  localisation_depot?: string | null
}

const props = defineProps<{
  procedure: ProcedureData
  suivi?: Partial<SuiviProcedure> | null
}>()

const shouldShowSuiviModification = (
  creationDate?: string | null,
  suiviModifiedDate?: string | null
) => {
  if (!suiviModifiedDate) return false
  if (props.suivi?.updated_by_name) return true
  return shouldShowModificationDate(creationDate, suiviModifiedDate)
}
</script>

<style scoped>
.procedure-metadata {
  width: 100%;
}
.metadata-timestamps strong {
  font-weight: 600;
}
</style>
