<template>
  <div class="premium-box fr-p-3w bo-card">
    <h3 class="fr-h6 fr-mb-2w bo-card-title">
      <span class="fr-icon-file-line fr-mr-1w"></span> Documents & Historique
    </h3>
    <div class="bo-flex-col--gap-1">
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

      <div class="bo-dashed-separator fr-mt-1w">
        <span class="fr-text--xs fr-mb-1v bo-text-mention-uppercase">Dernières mises à jour</span>
        <div class="fr-grid-row fr-grid-row--gutters fr-mt-1v">
          <div class="fr-col-6">
            <p class="fr-text--xs fr-mb-0 fr-text-mention--grey">Constatation</p>
            <p class="fr-text--sm fr-mb-0">
              <strong>{{ formatDate(procedure.modified) }}</strong>
            </p>
          </div>
          <div class="fr-col-6">
            <p class="fr-text--xs fr-mb-0 fr-text-mention--grey">Suivi de procédure</p>
            <p class="fr-text--sm fr-mb-0">
              <strong>{{ formatDate(procedure.suivi_procedure?.modified) }}</strong>
            </p>
          </div>
        </div>
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
