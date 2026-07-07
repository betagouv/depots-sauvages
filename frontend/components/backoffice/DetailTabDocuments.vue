<template>
  <div class="premium-box fr-p-3w bo-card">
    <h3 class="fr-h6 fr-mb-2w bo-card-title">
      <span class="fr-icon-file-pdf-line fr-mr-1w"></span> Documents de la Procédure
    </h3>
    <div class="bo-flex-col--gap-1">
      <!-- Rapport de constatation -->
      <div class="fr-p-1w bo-document-row">
        <div>
          <p class="fr-text--sm fr-mb-0"><strong>Rapport de constatation</strong></p>
          <p class="fr-text--xs fr-mb-0 fr-text-mention--grey">
            Généré le : {{ formatDate(procedure.doc_constat_generated_at) }}
          </p>
        </div>
        <a
          v-if="procedure.doc_constat_generated_at"
          :href="`/api/constatations/${procedure.id}/documents/doc_constat/`"
          target="_blank"
          class="fr-btn fr-btn--sm fr-btn--secondary fr-icon-download-line"
        >
          Télécharger
        </a>
        <span v-else class="fr-text--xs fr-text-mention--grey">Non généré</span>
      </div>

      <!-- Lettre d'information -->
      <div class="fr-p-1w bo-document-row">
        <div>
          <p class="fr-text--sm fr-mb-0"><strong>Lettre d'information</strong></p>
          <p class="fr-text--xs fr-mb-0 fr-text-mention--grey">
            Généré le : {{ formatDate(procedure.lettre_info_generated_at) }}
          </p>
        </div>
        <a
          v-if="procedure.lettre_info_generated_at"
          :href="`/api/constatations/${procedure.id}/documents/lettre_info/`"
          target="_blank"
          class="fr-btn fr-btn--sm fr-btn--secondary fr-icon-download-line"
        >
          Télécharger
        </a>
        <span v-else class="fr-text--xs fr-text-mention--grey">Non générée</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { formatDate } from '@/utils/date'

defineProps<{
  procedure: any
}>()
</script>
